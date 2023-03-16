#!/usr/bin/env python3

import json
import logging
import requests
import threading
import time
import socket
import sys
from datetime import datetime
from SpotterNetPositionObject import SNPosObject

TCP_IP = '127.0.0.1'
TCP_PORT = 2947
BUFFER_SIZE = 1024
START_MESSAGE = "?WATCH={\"enable\":true,\"json\":true}"
STOP_MESSAGE = "?WATCH={\"enable\":false}"
LOGIN_FILE = "/home/pi/SNPosition/SNLogin"
run = True
APPLICATION_ID = ""
seconds_since_update = 0.0
PosLock = threading.Lock()
oPosObject = SNPosObject
if len(sys.argv) > 1 and sys.argv[1] and sys.argv[1].lower() == '-i':
	logging.basicConfig(filename='SNPositionUpdate.log', level=logging.INFO)
else:
	logging.basicConfig(filename='SNPositionUpdate.log', level=logging.ERROR)
	
def LoadUserFile():
	global APPLICATION_ID
	loginfile = open(LOGIN_FILE)
	for line in loginfile:
		arLine = line.split("=")
		if arLine[0] == "APPLICATIONID":
			APPLICATION_ID = arLine[1]
		
def UpdatePos(dctPacket):
	global oPosObject
	if "time" in dctPacket.keys():
		oPosObject.SetTime(oPosObject, dctPacket["time"])
	else:
		logging.info('No data available for "time"')
		return
		
	if "lat" in dctPacket.keys():
		oPosObject.SetLat(oPosObject, dctPacket["lat"])
	else:
		logging.info('No data available for "lat"')
		return
	
	if "lon" in dctPacket.keys():	
		oPosObject.SetLon(oPosObject, dctPacket["lon"])
	else:
		logging.info('No data available for "lon"')
		return
		
	if "alt" in dctPacket.keys():
		oPosObject.SetElev(oPosObject, dctPacket["alt"])
		
	if "speed" in dctPacket.keys():
		oPosObject.SetSpeed(oPosObject, dctPacket["speed"]*2.23694)
		
	if "track" in dctPacket.keys():
		oPosObject.SetDirection(oPosObject, dctPacket["track"])
	
def POSTUpdate():
	global oPosObject
	if not oPosObject.Changed(oPosObject):
		return
			
	pload = {
				'id':APPLICATION_ID, 
				'report_at':oPosObject.Time(oPosObject).strftime('%Y-%m-%d %H:%M:%S'),
				'lat':oPosObject.Lat(oPosObject),
				'lon':oPosObject.Lon(oPosObject),
				'elev':oPosObject.Elev(oPosObject),
				'mph':oPosObject.Speed(oPosObject),
				'dir':oPosObject.Direction(oPosObject),
				'active':1,
				'gps':1
			}
	
	#print(pload)
	oRequest = requests.post("https://www.spotternetwork.org/positions/update", data = pload)
	if oRequest.status_code == 200:
		oPosObject.ResetChanged(oPosObject)
		logging.info('SN Updated at ' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'))
		return True
	else:
		logging.error('HTTP Status: ' + oRequest.status_code + '; Update not successfully sent to SN at ' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'))
		return False
	
	
def ConnectToGPSD():
	global PosLock
	global run
	oSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	oSocket.connect((TCP_IP, TCP_PORT))
	oSocket.send(START_MESSAGE.encode('utf-8'))

	while run:
		data = oSocket.recv(BUFFER_SIZE)
		arObjects = data.splitlines()
		for line in arObjects:
			#print(line)
			dctPacket = json.loads(line.decode('utf-8'))
			if dctPacket["class"] == "TPV":
				with PosLock:					
					UpdatePos(dctPacket)
						

def UpdateSpotterNetwork():
	global seconds_since_update
	global PosLock
	while run:
		if time.perf_counter() - seconds_since_update > 120:
			with PosLock:
				if POSTUpdate():
					seconds_since_update = time.perf_counter()

LoadUserFile()
if APPLICATION_ID:
	tGPSD = threading.Thread(target=ConnectToGPSD)
	tGPSD.start()

	tSNUpdate = threading.Thread(target=UpdateSpotterNetwork)
	tSNUpdate.start()

	tGPSD.join
	tSNUpdate.join

exit()
