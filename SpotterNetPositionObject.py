#!/usr/bin/env python

from datetime import datetime

class SNPosObject:
	time = datetime.today()
	lat = 0.0
	lon = 0.0
	elev = 0.0
	speed = 0.0
	direction = 0.0
	changed = False
		
	def __init__(self):
		self.time = datetime.today()
		self.lat = 0.0
		self.lon = 0.0
		self.elev = 0.0
		self.speed = 0.0
		self.direction = 0.0
		self.changed = False

	def SetTime(self, tTime):
		if self.time != datetime.strptime(tTime,"%Y-%m-%dT%H:%M:%S.%fZ"):
			self.time = datetime.strptime(tTime,"%Y-%m-%dT%H:%M:%S.%fZ")
			
	def Time(self):
		return self.time
			
	def SetLat(self, dLat):
		if self.lat != dLat:
			self.lat = dLat
			self.changed = True
	def Lat(self):
		return self.lat
			
	def SetLon(self, dLon):
		if self.lon != dLon:
			self.lon = dLon
			self.changed = True
			
	def Lon(self):
		return self.lon
			
	def SetElev(self, dElev):
		if self.elev != dElev:
			self.elev = dElev
			self.changed = True
			
	def Elev(self):
		return self.elev
			
	def SetSpeed(self, dSpeed):
		if self.speed != dSpeed:
			self.speed = dSpeed
			self.changed = True
			
	def Speed(self):
		return self.speed
		
	def SetDirection(self, dDir):
		if self.direction != dDir:
			self.direction = dDir
			self.changed = True
			
	def Direction(self):
		return self.direction
			
	def ResetChanged(self):
		self.changed = False
		
	def Changed(self):
		return self.changed
