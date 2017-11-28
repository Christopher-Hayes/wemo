# wemo
#### Note: This project is Python**2** compatible

## Folders

**docs**
Content on the repository website.

**netcam**
All Python files and files containing specific information about the netcam.

**switch**
Simple shell tool designed to interface with the WeMo switch. Contains relevant .xml docs as well.

**third_party_tools**
Tools used that were built by a third party.

**tools**
Unrelated tools built to facilitate the project.

**wemo**
Tool for normal interfacing to WeMo devices.

## All Files

### netcam

**netcam.py**
Used to interact with the Belkin NetCam and get data.

**netcam_gui.py**
Gives a live feed from the Wemo Netcam (in setup mode) using the mjpeg stream.

**netcam_info.txt**
Complete information about NetCam as produced by the Belkin AWS Server.

**netcam_known_tree.txt**
Partial tree of the netcam locally hosted http pages compiled over the course of this project.

### switch

**switch.py**
Interfaces to Belkin Switch, get and set functions.

**switch_shell.py**
User-friendly shell script for switch.py.

**switch_xml**
Compilation of relevant XML files a couple requests for easy viewing.

### third_party_tools

**miranda.py**
PnP library for getting information about PnP-capable devices on the network.
Note: this version is taken from another WeMo-related repository that altered the original library to be WeMo friendly. See comments at top of file.

### tools

**base_converter.py**
Simple tool that converts Base64 to UTF-8.

### wemo

**action.py**
Interface to most WeMo devices (Netcam excluded) using services and actions.
action.py parses the setup.xml searching for services.
That allows the program to find all possible actions from the relevant .xml files.

**action_shell.py**
User friendly shell script for action.py

**wemo_wifi.py**
Convenience tool that searches for a nearby WeMo network and can automatically change the device's wifi network.
Note: Only OS X compatible (uses Airport), user also has to have Airport enabled.
