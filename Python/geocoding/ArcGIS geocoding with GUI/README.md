# ArcGIS Geogoder

## How to use it?

### 1. Choose import file
Import file requires special fields: **ID_TT**, **Client**, **Address** 

![Required fields-1](https://github.com/fugrusha/blackhole/blob/pyqt_gui/Python/geocoding/ArcGIS%20geocoding%20with%20GUI/images/Required%20fields-1.png)

or **ID_TT**, **Client**, **Region**, **City**, **Street**, **NoHouse**

![Required fields-2](https://github.com/fugrusha/blackhole/blob/pyqt_gui/Python/geocoding/ArcGIS%20geocoding%20with%20GUI/images/Required%20fields-2.png)

### 2. Select parameters
* Start index - defines from which row start to geocode
* Write data rate - how often the program saves a backup file
* Attempts to geocode - how many times the program tries to geocode an address before it gives up

### 3. Push Search button
Output excel-file is created on your Desktop


## What's inside?

There are 4 main parts:
* *QtWindow.py* - main module which runs app
* *mydesign.py* - module with GUI
* *main_geo_module.py* - module which is supposed to import excel-file, define coords and return excel-file with coords
* *images_rc.py* - module with icons, images as resource

Other additonal files:
* *main.spec* - spec-file for pyinstaller
* *images.qrc* - file with resources, images
* *src2py.bat* - convert qrc to python
* *GUI.ui* - file with GUI (from QtDesigner)
* *ui2py.bat* - convert ui to python

## How to create exe-file

### Run virtual environment
You can use virtualenv or install Win10 in Virtual Box. Just install win10 and Python on it. I chose second variant.

#### Using virtualenv (if you want)
Firsly, open present work directory in cmd:

`cd C:\Users\andre\Anaconda3\Scripts\my_scripts\`

Install virtualenv:

`pip install virtualenv`

Run virtual environment:

`virtualenv ENV_NAME`

Open folder:
 `env\Scripts\activate`

Then, you can install nesaccery libs via pip: install

`pip install pyinstaller`


## Create exe-file with pyinstaller
On your virtual machine you have to install all necessary packages.

Then open cmd and paste:

`pyinstaller --onedir --onefile main.spec`

My specfile you can find above.
