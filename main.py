import tkinter as tk
import re
import subprocess
from os import getcwd
from src.scripts import \
		select_routes_gpx_file, \
		create_routing_points_xml, \
		create_favourites_xml, \
		push_file_to_tablet
from sys import exit


def get_device_id():
	'''
	Get device ID from connected device. To run this, platform-tools needed
	to be located inside the root project folder. Adb will run and fetch the
	connected device ID. Additionally pc must be authorized to access the device,
	via USB debbuging enabled option.
	'''
	cwd = re.sub(r"\\","/",getcwd())
	adb_command = f'{cwd}/platform-tools/adb.exe'
	adb_output = subprocess.check_output([adb_command,"devices"])
	id = re.search(r"attached\\r\\n(\w+)\\t",str(adb_output)).group(1)
	DEVICE_ID.set(id)
	print(f'DeviceID: {id} connected')

def parseFile():
	'''
	Select gpx file
	'''
	fname = select_routes_gpx_file()
	ROUTE_FILE.set(fname)

# Tkinter Initialization
form = tk.Tk()
form.geometry('360x160')
form.wm_title('Route Importing Tools v2.0')

# Variables that need to be stored
ROUTE_FILE = tk.StringVar()
DEVICE_ID = tk.StringVar()

Lb1 = tk.Label(form, text='Please select .xml files: ')
Lb1.grid(row=0, column=0, sticky='WE', padx=10, pady=5)

Btn1 = tk.Button(form, text="GET DEVICE ID", bg = '#AAAAFF', \
	command = lambda: get_device_id())
Btn1.grid(row=0, column=1, sticky='WE', padx=10, pady=5)

Btn2 = tk.Button(form, text="SELECT FILES", bg = '#AAAAFF', \
	command = lambda: parseFile())
Btn2.grid(row=1, column=0, columnspan=2 ,sticky='WE', padx=10, pady=5)

Btn3 = tk.Button(form, text="CREATE ROUTES XML" , bg = '#d3d3d3', \
	command= lambda: create_routing_points_xml(ROUTE_FILE.get()))
Btn3.grid(row=2, column=0, sticky='WE', padx=10, pady=5)

Btn4 = tk.Button(form, text='CREATE FAV XML', bg = '#d3d3d3', \
	command= lambda: create_favourites_xml(ROUTE_FILE.get()))
Btn4.grid(row=2, column=1, sticky='WE', padx=10, pady=5)

Btn5 = tk.Button(form, text='PUSH ROUTES FILE', bg = '#00FF00', \
	command = lambda: push_file_to_tablet(DEVICE_ID.get(),"routing_points.xml"))
Btn5.grid(row=3, column=0, sticky='WE', padx=10, pady=5)

Btn6 = tk.Button(form, text='PUSH FAVOURITES FILE', bg = '#00FF00', \
	command = lambda: push_file_to_tablet(DEVICE_ID.get(),"favourites.xml"))
Btn6.grid(row=3, column=1, sticky='WE', padx=10, pady=5)

Btn7 = tk.Button(form, text="EXIT" , command= lambda: exit())
Btn7.grid(row=3, column=2,padx=10, pady=5,sticky= 'E')

tk.mainloop()