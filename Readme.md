What ::

An arduino based tracking system. It consists of a tracker which communicates its location to a server (Google App-Engine). The location is shown on a iframe embedded google map.

The server page can be seen at http://www.arduinogpsproject.appspot.com


How ::

The tracker consists of Arduino, GPS Reciever and a GSM/GPRS Shield. The communication was supposed to happen through GPRS.


Why Serial_to_Server.py ::

Because I am having trouble making GPRS shield work (I am not currently adept with AT Commands), I am using the arduino's USB connection and my laptops internet connection to send the location data to the server. This is what Serial_to_Server.py does.

I hope to get GPRS working soon.