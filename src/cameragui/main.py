from pathlib import Path
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from cameragui.view import View
from cameragui.model import Model
from cameragui.controller import Controller

def main():
    # Set up:
    # Ask user for: 
    # - path to image folders
    # - path to annotation schema
    # - path to save annotation table
    # - number of images to display at once
    # - which image to annotate
    # - number of processes to use to load images (optional)

    # example setup:
    project_root = Path(__file__).parent.parent.parent
    img_path_format = str(project_root / "example_data/camera/P*/*.JPG")
    schema_path = str(project_root / "example_data/example_schema.csv")
    save_path = str(project_root / "example_data/example_annotion.csv")

    n_display_images = 3
    image_index = 1 # annotate the second image (zero-indexed)
    n_processes = 4 

    # GUI setup
    root = Tk()
    root.title("Camera logger annotation tool")
    view = View(root)
    model = Model(
        img_path_format, 
        n_display_images,
        image_index, 
        schema_path, 
        save_path, 
        view,
        n_processes,
    )
    controller = Controller(model, view)

    # lastly, start the GUI
    root.mainloop()



if __name__ == "__main__":
    main()