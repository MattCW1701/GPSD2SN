# GPSD2SN
Copyright (C) 2021 Matthew Wann KG4GUF
A Python script that transmits a user's position from GPSD to Spotter Network

LICENSE
This software is distributed under the terms of the BSD 0-clause license
A copy of this license should have been provided. If not, please go to https://opensource.org/licenses/0BSD

INSTALLATION
Place the three files (two .py, one plain file) in any directory you can execute from.
Add your Spotter Network application id after the equal sign in the plain file.
Run the script by whatever means you desire. By default, errors are logged, but if more information is desired, run the script with a -i argument.
As written there is no means of stopping the script so it must be manually terminated.

NOTES
The way this works is by requesting GPSD to update position in the JSON format. Whenever this is received, the information is stored in the position object.
Every two minutes, an attempt is made to update Spotter Network with the current position. Two minutes was chosen based on feedback on the StormTrack forum
