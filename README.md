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
  * choose if you want your data organized in np arrays for easy use - Two forms (np array contining pixel_array of dcm or np array containing path to each dcm Folder)
  * Optionally: 
    * choose a color map 
    * change iterpolation to your liking 

## New Features: 
  * a variables for _makeDirArrays_ and _makeNpArrays_ was added for saving your organized data into np arrays of the dcm image/path arrays if you want to use your data in a different way
  * to make it easier to do ml work, now you can save your data as simplified arrays in two forms: 
    * if you set _makeDirArrays_ to **TRUE* this will create an np array with the path to each dcm under that particular classification 
    * if you set _makeNpArrays_ to **TRUE* this will create an np array with the path to each dcm under that particular classification  
      * *** NOTE: when using the makeNpArrays option if your data is very large it may be hard to save the np array (e.g. not recommended for large data sets of CT scans --> use makeDirArrays, and extract the pixel_array for your use later, if its a single scan e.g. a radiograph/DX/CR/SR this should be managable) ***  
 * all .npy files generated will be stored in a folder called ** FolderOfNpArrays ** under the classificationMainDirectory
## Running: 
  * run the program (python/python3 MlDataOrganizer.py) - Python 3 is recommended 
  * on the right side there is a browse button click that and select the directory that contains all your cases 
  * Then you can pick any folder and view the images 
  * Use the slider at the bottom to view all parts of the dcm
  * Select the "class" that the .dcm fits under and this will move the data into that folder for easy organization  
  * The image is moved to the corresponding folder and viewer is updated
  * If _makeDirArrays_ or _makeNpArrays_ features are used, path to dcm and pixel_array of image (respectivly) are saved and stored in a .npy file for convenience 

## NOTES: 
  * backupdata - is a folder that contains DCM it is there for you to copy and replace folders in sample data while testing 
  
## Future: 
   * json creation for nvidia Clara 
   * ~~ removing need for default image ~~ (completed may 3)
