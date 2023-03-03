from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from cameragui.constants import *

class View:
    """
    Basic layout of the GUI.
    """
    def __init__(self, root):
         
        # content is a 2 row by 2 column grid
        content = ttk.Frame(root) # create a frame to hold the content
        content.grid(column=0, row=0) # add to root

        # =================== Schema Frame  =================== (left)
        # create a frame for annotations on the left
        self.schema_holder = ttk.Frame(content, padding=FRAME_PAD)
        self.schema_holder.grid(column=0, row=0, rowspan=2, sticky="ns")
        self.schema_frame = ttk.Frame(self.schema_holder, padding=SUBFRAME_PAD, borderwidth=BORDER_WIDTH, relief="solid")
        # add padding to the left and right 
        self.schema_frame.grid(column=0, row=0, sticky="n")
        
        # -> model will update schema frame to show available labels

        # =================== Image Frame =================== (top right)
        # create a frame for images on the right
        self.image_frame = ttk.Frame(content, padding=FRAME_PAD)
        self.image_frame.grid(column=1, row=0)

        # add placeholder text saying Images loading... which will be replaced by images
        self.image_placeholder_text = ttk.Label(self.image_frame, text="Images loading...")
        self.image_placeholder_text.grid(column=0, row=0)

        # -> model will update image frame to show images

        # =================== Input Frame =================== (bottom right)
        # create a frame for the annotation input at the bottom
        self.input_frame = ttk.Frame(content, padding=FRAME_PAD)
        self.input_frame.grid(column=1, row=1)


        # =================== Current annotations
        # add frame at top to display current annotations
        self.current_annot_frame = ttk.Frame(self.input_frame, padding=SUBFRAME_PAD)
        self.current_annot_frame.grid(column=0, row=0)

        ttk.Label(self.current_annot_frame, text="No annotations").grid(column=0, row=0)


        # look at the current row in the annotation table
        # for all label columns with a value > 0.0, add a label to the frame

        # -> controller will update current_annot_frame to show current annotations
        # def update_current_annot_frame():
        #     global current_row
        #     for child in current_annot_frame.winfo_children():
        #         child.destroy()
        #     i = 0
        #     for label, confidence in zip(labels, annotation_df.loc[current_row, labels]):
        #         if confidence > 0.0:
        #             ttk.Label(current_annot_frame, text=f"{label}: {confidence}").grid(column=0, row=i)
        #             i+=1
        # update_current_annot_frame()

        # =================== Annotation input
        # add frame in middle where annnotations can be added
        self.annot_input_frame = ttk.Frame(self.input_frame, padding=SUBFRAME_PAD)
        self.annot_input_frame.grid(column=0, row=1)

        ttk.Label(self.annot_input_frame, text="Loading controls...").grid(column=0, row=0)

        
        # controller will populate annotation_input_frame with widgets
           
        # # Add label to the left saying "Add annotation:"
        # ttk.Label(annot_input_frame, text="Add annotation:").grid(column=0, row=0)
        # # Add a combobox to the right to select the label, TODO combobox with autocomplete
        # label_combobox = ttk.Combobox(annot_input_frame, values=labels)
        # label_combobox.state(["readonly"]) # means can only go with the options
        # label_combobox.grid(column=1, row=0)
        # # Add a label to the right saying "confidence:"
        # ttk.Label(annot_input_frame, text="confidence:").grid(column=2, row=0)
        # # Add entry box to the right accepting a float between 0 and 1
        # d = DoubleVar(value=1.0)
        # confidence_entry = ttk.Entry(
        #     annot_input_frame, 
        #     text=d, # default value
        #     # check that value is float: see zip example
        #     # check the value when no longer entering text
        #     # if value is invalid, make it not possible to add annotation
        #     # this can be done by disabling the add button
        # )
        # confidence_entry.grid(column=3, row=0)
        # # Add button to the right to add the annotation
        # def add_annotation():
        #     # get the label and confidence from the combobox and entry box
        #     label = label_combobox.get()
        #     confidence = confidence_entry.get()
        #     # add the annotation to the annotation table
        #     annotation_df.loc[current_row, label] = confidence
        #     # update the current annotation frame
        #     update_current_annot_frame()
        #     # update the current row
        #     current_row += 1
        # add_button = ttk.Button(annot_input_frame, text="Add", command=add_annotation)
        # add_button.grid(column=4, row=0)
        

        # =================== Comments input
        # add frame at bottow where comments can be added
        self.comment_frame = ttk.Frame(self.input_frame, padding=SUBFRAME_PAD)
        self.comment_frame.grid(column=0, row=2)

        # controller will populate annotation_input_frame with widgets
        # in meanwhile have label placeholder saying "Comments:"
        ttk.Label(self.comment_frame, text="Loading space for comments...").grid(column=0, row=0)