#!/usr/bin/env python

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as plt
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider
matplotlib.use('TkAgg')

import PySimpleGUI as sg

import numpy as np
from numpy import random

import pydicom as dicom

import shutil
import os 




#Sample image sourced at : https://www.visus.com/en/downloads/jivex-dicom-viewer.html

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
classNames = ["Low Damage", "Medium Damage", "High Damage"]
classificationMainDirectory = "/Users/admin/Documents/DataOrganizerGit/MLdataOrganizer/"
colorMap = "hot"
interpolation="nearest"


# ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE -------------------------------

for folder in classNames:
    path = os.path.join(classificationMainDirectory,folder)
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            print("Folders could not be made")
            exit() 

buttonEvents = ["{0}".format(i) for i in range(len(classNames))]
images = []
data = []
pathDir = ''
randomImage = np.tile(np.arange(256).reshape(16,16), (16,16)) * 4
currentidx = 0 
fig, ax = plt.subplots(figsize=(6, 6), dpi=160)
fig.subplots_adjust(bottom=0.15)
im_h = ax.imshow(randomImage, cmap=colorMap, interpolation=interpolation)
firstImage = True 

# -------------------------------  MATPLOTLIB functions -------------------------------
def updateImage(newDir):
    global data 
    global pathDir
    pathDir = newDir + "/"
    images = os.listdir(pathDir)
    data = [dicom.read_file(pathDir + s, force=True) for s in images]
    try: 
        data = sorted(data, key=lambda s: s.SliceLocation)
    except:
        pass 
    currentidx = 0 
    picture = data[currentidx].pixel_array
    im_h.set_data(picture)
    fig.canvas.draw()
    fig.canvas.flush_events()
    updatedLength = len(data)-1
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
    folder = classNames[int(index)]
    newDir = os.path.join(classificationMainDirectory,folder)
    print("moving to", newDir)
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
    [sg.Button(classNames[i], enable_events=True, key=str(i)) for i in range(len(classNames))]
]

Other_stuff_column=[
    [sg.Text("Other features like annotation go here:")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.VSeperator(),
        sg.Column(Other_stuff_column)
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
        if not firstImage: 
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
        try:
            updateImage(values["-FILE LIST-"][0])
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