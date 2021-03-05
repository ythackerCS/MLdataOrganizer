# MLdataOrganizer

## Introduction

> Dataset organization and processing is probably the most annoying part of ml. Data set organization is still limited I wanted to make something that would let you view dcm and easily pick its "classification."  This tool allows you to view dicom and then sort data into "class" folders for ML.

##  Design: 
  * Used python 
  * Pythonsimplegui (hoping to transition to tkinter later) 

##  How to use:
  > All the variables that should need altering for use should be in the "#--- stuff script will need to be provided:" region 
  * provide classNames - these will be the folders that will be made for classification 
  * provide a main classification directory - this is the main directory where the classification folders wil be stored 
  * Optionally: 
   * choose a color map 
   * change iterpolation to your liking 
  
## Running: 
  * run the program 
  * on the right side there is a browse button click that and select the directory that contains all your cases 
  * Then you can pick any folder and view the images 
  * Use the slider at the bottom to view all parts of the dcm
  * Select the "class" that the .dcm fits under and this will move the data into that folder for easy organization  
  * The image is moved to the corresponding folder and viewer is updated

## NOTES: 
  * backupdata - is a folder that contains DCM it is there for you to copy and replace folders in sample data while testing 
  
## Future: 
   * json creation 
   * removing need for default image
