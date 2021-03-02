#!/usr/bin/env python
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
import shutil
import numpy as np
import pydicom as dicom
import matplotlib.pylab as plt
import os 
from matplotlib.widgets import Slider



"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.
Basic steps are:
 * Create a Canvas Element
 * Layout form
 * Display form (NON BLOCKING)
 * Draw plots onto convas
 * Display form (BLOCKING)
 
 Based on information from: https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
 (Thank you Em-Bo & dirck)
"""
#--- stuff script will need to be provided: 
classes=7
foldersAsscociatedWithClasses = ["/Users/admin/Documents/DataOrganizerGit/MLdataOrganizer/TestFolder", "/Users/admin/Documents/DataOrganizerGit/MLdataOrganizer/TestFolder2"] 
buttonEvents = ["{0}".format(i) for i in range(classes)]
colorMap = "hot"
interpolation="nearest"


# ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE -------------------------------

pathDir = '/Users/admin/Documents/DataOrganizerGit/MLdataOrganizer/sample_data/Case D/'
images = os.listdir(pathDir)
data = []
for s in images:
    if s.endswith('.dcm'):
        data.append(dicom.read_file(pathDir + s, force=True))
try: 
    data = sorted(data, key=lambda s: s.SliceLocation)
except:
    pass

currentidx = 0 
fig, ax = plt.subplots(figsize=(6, 6), dpi=160)
fig.subplots_adjust(bottom=0.15)
im_h = ax.imshow(data[currentidx].pixel_array, cmap=colorMap, interpolation=interpolation)
firstImage = True 

# -------------------------------  MATPLOTLIB functions -------------------------------
def updateImage(newDir):
    global data 
    global pathDir
    pathDir = newDir + "/"
    images = os.listdir(pathDir)
    # print(images)
    data = [dicom.read_file(pathDir + s, force=True) for s in images]
    try: 
        data = sorted(data, key=lambda s: s.SliceLocation)
    except:
        pass 
    currentidx = 0 
    # print("data lenth:", len(data))
    picture = data[currentidx].pixel_array
    im_h.set_data(picture)
    fig.canvas.draw()
    fig.canvas.flush_events()
    updatedLength = len(data)-1
    # print(updatedLength)
    window["-SLIDER-"].Update(range = (0,updatedLength))
    window.refresh()

def update_depth(val):
    global data 
    new = int(round(val))
    im_h.set_data(data[new].pixel_array)
    fig.canvas.draw()
    fig.canvas.flush_events()
    return fig 

def mouse_wheel(event):
    global currentidx
    if event.step < 0:
        if(currentidx == len(data)-1):
            currentidx = 0
        currentidx += 1

    if event.step > 0:
        if(currentidx == 0):
            currentidx = len(data)-1
        currentidx -= 1
    update_depth(currentidx)

def moveTo(index):
    currnentDir = pathDir
    newDir = foldersAsscociatedWithClasses[int(index)]
    shutil.move(currnentDir, newDir)
    window["-FILE LIST-"].update(fnames)
    window.refresh()

# ------------------------------- Beginning of Matplotlib helper code -----------------------

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw() 
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=0)
    if not firstImage:
        return figure_canvas_agg

# ------------------------------- Beginning of GUI CODE -------------------------------

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(30, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(50, 30), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen

image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(0, 0), key="-TOUT-")],
    [sg.Canvas(key='-CANVAS-')],
    [sg.Slider((0, len(data)-1), orientation='h', size=(80, 10), enable_events=True, key='-SLIDER-')],
    [sg.Button("Class "+str(i+1), enable_events=True, key=str(i)) for i in range(classes)]
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

# create the form and show it without the plot
window = sg.Window('Data Organizer for ML applications', layout, finalize=True, element_justification='center', font='Helvetica 18')

# add the plot to the window
fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

while True:
    event, values = window.read()
    # print(event)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-SLIDER-":
        fig = update_depth(values['-SLIDER-'])
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    elif event == "-FOLDER-":
        folder = values["-FOLDER-"]
        fnames = []
        dataFolder = os.listdir(folder)
        for files in dataFolder:
            folder_path = (os.path.join(folder, files))
            if os.path.isdir(folder_path):
                file_contents = os.listdir(folder_path)
                for files in file_contents:
                    if files.lower().endswith(".dcm"):
                        if folder_path not in fnames: 
                            fnames.append(folder_path)
        window["-FILE LIST-"].update(fnames)

    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        firstImage = False
        # print("chose file")
        try:
            # print("new value picked:", values["-FILE LIST-"][0])
            updateImage(values["-FILE LIST-"][0])
            # print("data length in loo",len(data))
        except:
            pass
    elif event in buttonEvents:
        moveTo(event)
        folder = values["-FOLDER-"]
        fnames = []
        dataFolder = os.listdir(folder)
        for files in dataFolder:
            folder_path = (os.path.join(folder, files))
            if os.path.isdir(folder_path):
                file_contents = os.listdir(folder_path)
                for files in file_contents:
                    if files.lower().endswith(".dcm"):
                        if folder_path not in fnames: 
                            fnames.append(folder_path)
        window["-FILE LIST-"].update(fnames)
        window["-FILE LIST-"].update(fnames)
        window.refresh()
window.close()