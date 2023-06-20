import xml.etree.ElementTree as ET
from os.path import split
from tkinter import filedialog
from ppadb.client import Client as AdbClient
from src import waypoint

def select_routes_gpx_file():
	'''
	File dialog to select a gpx file with routes and favorites.
	'''
	rfile = filedialog.askopenfilename()
	error=False
	print(rfile)
	fpath , fname = split(rfile)
	if fname[-3:] != 'gpx':
		error=True
	if error:
		messagebox.showwarning("Warning",'!!!You have selected non .gpx files!!!Please select again.')
	print(f'Route file: "{fname}" is selected')
	return rfile

def create_routing_points_xml(rfile):
	'''
	Creates specific format routing_points.xml file that will be imported to Navigator.
	'''
	ROUTES = 0
	rp = open('data/routing_points.xml','w')
	rp.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
	rp.write('<routing_points>\n')

	fpath , fname = split(rfile)
	w = waypoint.waypoint()
	# Parse the file
	tree = ET.parse(rfile)
	root = tree.getroot()
	
	# <rte> stands for route in the gpx file
	for rte in root.findall('{http://www.topografix.com/GPX/1/1}rte'):
		ROUTES +=1
		rp.write('\t<set>\n')
		rp.write('\t\t<name>'+fname[:-4]+'_'+rte.find('{http://www.topografix.com/GPX/1/1}name').text+'</name>\n')
		i=0
		# Loop through all <rte> children with tag <rtept> which
		# stands for route point.
		for wpt in rte.findall('{http://www.topografix.com/GPX/1/1}rtept'):
			w.lat = wpt.attrib.get('lat')
			w.lon = wpt.attrib.get('lon')
			# First will be START
			if i == 0:
				w.name = 'START'
				rp.write(w.wpt_to_xml_route(0)+'\n')
			# Last will be END
			elif i == (len(rte.findall('{http://www.topografix.com/GPX/1/1}rtept'))-1):
				w.name = 'END'
				rp.write(w.wpt_to_xml_route(2)+'\n')
			# All the others will be normal points
			else:
				w.name = 'W'+str(i)
				rp.write(w.wpt_to_xml_route(1)+'\n')
			i+=1
		rp.write('	</set>\n')
	rp.write('</routing_points>\n')
	print(ROUTES,'routes were added to routing_points XML')

def create_favourites_xml(rfile):
	'''
	Creates specific format favourites.xml file that will be imported to Navigator .
	'''
	SITES = 0
	rp = open('data/favourites.xml','w')
	rp.write('<?xml version="1.0" encoding="utf-8"?>\n')
	rp.write('<favourites version="1">\n')
	i=0
	w = waypoint.waypoint()
	tree = ET.parse(rfile)
	root = tree.getroot()
	for wpt in root.findall('{http://www.topografix.com/GPX/1/1}wpt'):
		SITES+=1
		w.lat = wpt.attrib.get('lat')
		w.lon = wpt.attrib.get('lon')
		w.name = wpt.find('{http://www.topografix.com/GPX/1/1}name').text
		rp.write(w.wpt_to_xml_favourite()+'\n')
		i+=1
	rp.write('</favourites>\n')
	print(SITES,'sites were added to favourites XML')

def push_file_to_tablet(device,file):
	'''
	Sends one file at a time to device specific backup folder.
	'''
	client = AdbClient(host="127.0.0.1", port=5037)
	device = client.device(device)
	BACKUPS_FOLDER = "/storage/emulated/0/Navigator/MapFactor\ Navigator\ Backups/"
	backups = device.shell(f'cd {BACKUPS_FOLDER};ls')
	backups = backups.split()

	if file in ["routing_points.xml","favourites.xml"]:
		ROUTING_POINTS = "/storage/emulated/0/Navigator/MapFactor Navigator Backups/" \
						+ backups[0] + "/" + file
		device.push("data/" + file, ROUTING_POINTS)
		print(file, 'uploaded!!!')
	else:
		print('Error XML File Not Found')




