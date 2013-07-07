import serial
from datetime import datetime
import json
import requests


#date = datetime.strptime(out_line[1].strip(), '%m/%d/%Y-%I/%M/%S.0') 
data = {}
url = 'http://www.arduinogpsproject.appspot.com/update'
device = '/dev/tty.usbmodemfd121'
arduino = serial.Serial(device, 4800)
while 1:
	arduino.flushInput()
	serial_out = arduino.readline()
	while 'done' not in serial_out:
		print serial_out
		out_line = serial_out.split(':')
		if 'date' in out_line[0]:
			data.update({out_line[0]:out_line[1].strip()})
		else:
			data.update({out_line[0]:float(out_line[1].strip())})
		serial_out = arduino.readline()
	response = requests.post(url, params = data)
	print response.text
	print data