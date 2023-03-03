# Simple image annotation

## Installation
This uses pandas, and pillow as modules
It allso uses tkinter. To make this work on mac, I had to use `brew install python-tk@3.11`. 

## Flow
- Point to directory of format:
```
camera/ P001/   img1<timestamp>.JPG
                img2<timestamp>.JPG
                ...
        P002/   img1<timestamp>.JPG
                ...
        ...
```
- Currently `<timestamp>` has to be of format `20141003_121214E` meaning 2014, 10th month, 03 day, 12h12m14sec (what is E?)
    - Generalise this to also parse images with any file names, or images with some numeric information.
- Point to schema 
- Specify save directory for annotations
    - Implement autosaving as annotation goes on
    - Eventually have option to continue with previous annotation project
- Allow user to:
    - view `N` images at a time,
    - choose which image to annotate (1-N), e.g. annotate middle or last image.
- Diplay:
    - images,
    - schema,
    - time image was taken,
    - time between images (potentially exclude images if too much time has elapsed),
    - progress bar,
    - suggested similar sequences of images.
- Input:
    - Allow user to add annotations to each,
    - Allow user to add comments,
    - Allow keyboard shortcuts,
    - Allow tab for autocomplete,
    - Allow multiple annotations,
    - Allow uncertainty.

## Commands
- next/previous annotation
- add/remove annotation from image
- manually save annotation
    - potentially to a different folder
- add/edit comments
- undo?

## Data representation
Under the hood, we will have a pandas dataframe that looks like
```
time            | id    | path  | comments  | label0        | label1        | ...   | label N       |
np.datetime64   | int   | str   | str       | float [0,1]   | ditto label0  | ...   | ditto label0  |
```

