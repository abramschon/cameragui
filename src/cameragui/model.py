from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from cameragui.view import View
from cameragui.annotation import create_annot_table, save_annot_table, load_annot_table
from cameragui.schema import parse_schema
from cameragui.image import process_imgs
from cameragui.constants import *

class Model:
    """
    The model is centered around a pandas dataframe, the `annotation_df` that stores the annotations.
    It contains methods that update and load data from this dataframe.
    It is updated by the contoller (which receives inputs from the user) and it is responsible 
    for handling representations of the data in the view which are not interacted with by the user.
    """
    def __init__(
            self, 
            img_path_format: str, 
            n_display_images: int,
            image_index: int, # of the n displayed images, which image to annotate
            schema_path: str, 
            save_path: str, 
            view: View,
            n_processes: int = 4,
            rotate_image: int = -90,
        ):
        
        # Class attributes
        self.n_display_images = n_display_images
        self.image_index = image_index # also how many images to display to the left of the current image
        self.images_to_right = n_display_images - image_index - 1
        self.rotate_image = rotate_image
        self.save_path = save_path
        self.view = view
        self.row = image_index
        
        # =============== Initialise pandas dataframe
        # load images
        img_df = process_imgs(img_path_format, n_processes=n_processes)
        # load schema
        self.labels = parse_schema(schema_path)
        # Initialise annotation table
        annotation_df = create_annot_table(img_df, self.labels)
        # sort annotation df by ID, then time
        annotation_df = annotation_df.sort_values(by=["id", "time"])
        self.annotation_df =  annotation_df.reset_index(drop=True)

        # =============== Initialise view
        self.init_schema_frame() # populates the schema frame with labels
        self.display_images() # displays the initial images in the image frame


    def init_schema_frame(self):
        """
        Displays the parsed labels in the schema frame as a list of labels
        """
        # add label at the top saying "Annotations:"
        ttk.Label(self.view.schema_frame, text="Annotations:").grid(column=0, row=0)
        # add frame to save labels
        label_frame = ttk.Frame(self.view.schema_frame)
        label_frame.grid(column=0, row=1)
        for i, label in enumerate(self.labels):
            ttk.Label(label_frame, text=label).grid(column=0, row=i)
        # add scrollbar if length of annotations exceeds the height of the screen
        # TODO
    
    def display_images(self):
        """
        Displays the images in the image frame of the view.
        Images start at the current row and includes self.image_index images to the left and self.images_to_right images to the right.
        Returns true if the images were displayed and false if there are no more images to display.
        """
        if self.row + self.images_to_right >= len(self.annotation_df):
            return False
        
        # clear the image frame
        for widget in self.view.image_frame.winfo_children():
            widget.destroy()


        self.images_on_screen = [] # need pointers to current images on display, otherwise they get garbage collected
        # add self.n_display_images frames to the view.image_frame
        for i in range(self.n_display_images):
            img_index = self.row - self.image_index + i
            # add frame
            image_box = ttk.Frame(self.view.image_frame, padding=ELEMENT_PAD)
            if i == self.image_index:
                image_box.config(borderwidth=BORDER_WIDTH, relief="solid")
            image_box.grid(column=i, row=0)

            # read image and timestamp from dataframe 
            image = Image.open(self.annotation_df.loc[img_index, "path"])
            image = image.rotate(self.rotate_image, expand=True)
            image = self.resize_image(image)
            img = ImageTk.PhotoImage(image)
            self.images_on_screen.append(img)
            
            timestamp = self.annotation_df.loc[img_index, "time"]
            # format timestamp to display day and time as day, %d day %Hh%M:%S
            timestamp = timestamp.strftime("Day %d, %Hh%M:%S")
            

            # add label with timestamp above image, centered
            ttk.Label(image_box, text=timestamp).grid(column=0, row=0)

        
            ttk.Label(image_box, image=self.images_on_screen[-1]).grid(column=0, row=1)


        return True


    def add_annotation(self, label, confidence):
        if label not in self.labels:
            return False
        try:
            confidence = float(confidence)
            if confidence < 0 or confidence > 1:
                return False
        except ValueError:
            return False
        self.annotation_df.loc[self.row, label] = confidence
        return True # now controller must update view with label buttons
    
    def remove_annotation(self, label):
        if label not in self.labels:
            return False
        self.annotation_df.loc[self.row, label] = 0
        return True

    def get_nonzero_annotations(self):
        """
        Returns a list of labels that have been annotated
        """
        row_label_data = self.annotation_df.loc[self.row, self.labels]
        non_zero = row_label_data[row_label_data > 1e-5]
        confidences = non_zero.values.tolist()
        labels = non_zero.index.tolist()
        return labels, confidences

    def next_row(self):
        """
        Move to next row to annotate
        Importanly, check that we have not reached the end of the dataframe, and also
        check that all images belong to the same participant.
        """
        
        # TODO also need to jump between participants

        self.row += 1
        # update View to display next set of images
        return True

    def save_annotations(self):
        save_annot_table(self.annotation_df)

    # TODO, understand under which circumstances reloading is needed

    def resize_image(self, image, min_size = (400,300)):
        """
        Resize image so that n_display images fit side by side in the image_frame.
        Maintain aspect ratio of the images.
        """
        # get width and height of image frame
        image_frame = self.view.image_frame
        max_width = max(image_frame.winfo_width() // self.n_display_images, min_size[0])
        max_height = max(image_frame.winfo_height(), min_size[1])
        # calculate size of each image
        resize_ratio = min(max_width / image.width, max_height / image.height)
        image = image.resize((int(image.width * resize_ratio), int(image.height * resize_ratio)), Image.ANTIALIAS)

        return image
    
    # ================= Comment getters and setters
    def get_comment(self):
        return self.annotation_df.loc[self.row, "comment"]
    
    def set_comment(self, comment):
        self.annotation_df.loc[self.row, "comment"] = comment
        return True
