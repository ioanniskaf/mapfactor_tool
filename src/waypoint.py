class waypoint:
	'''
	Waypoint class. Contructor with only name, latitude, longitude.
	'''
	def __init__(self,name=0,lat=0,lon=0):
		self.name = name
		self.lat = lat
		self.lon = lon

	def wpt_to_xml_route(self,type):
		'''
		Method to translate <wpt> (from gpx file) to waypoint
		that will be used to create the routing xml file for the Navigator.
		'''
		wlat = int(3600000*float(self.lat))
		wlon = int(3600000*float(self.lon))
		# Three types will be used for START, END and in between route waypoints.
		if type == 0:
			wpt = ('\t\t<departure><name>'+self.name+'</name><lat>'+str(wlat)+'</lat><lon>'+str(wlon)+'</lon></departure>')
		elif type == 1:
			wpt = ('\t\t<waypoint><name>'+self.name+'</name><lat>'+str(wlat)+'</lat><lon>'+str(wlon)+'</lon></waypoint>')
		elif type == 2:
			wpt = ('\t\t<destination><name>'+self.name+'</name><lat>'+str(wlat)+'</lat><lon>'+str(wlon)+'</lon></destination>')
		return wpt

	# Method to translate <wpt> (from gpx file) to waypoint
	# that will be used to create the favorites xml file for the Navigator.
	def wpt_to_xml_favourite(self):
		wlat = int(3600000*float(self.lat))
		wlon = int(3600000*float(self.lon))
		wpt = ('<item name="'+self.name+'" lat="'+str(wlat)+'" lon="'+str(wlon)+'"/>')
		
		return wpt