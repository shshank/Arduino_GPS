#!/usr/bin/env python

import webapp2
import datetime
from datetime import datetime, timedelta
from google.appengine.ext import ndb


LOCATION_NAME = 'arduino'

PAGE_HEAD = '<!DOCTYPE html><html><head><title>GPS Tracking</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><!-- Bootstrap --><link href="http://localhost:9000/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen"></head>'


def location_key(location_name=LOCATION_NAME):
    return ndb.Key('location_name', LOCATION_NAME)

class Location(ndb.Model):
    #lid
    lat = ndb.FloatProperty()
    lng = ndb.FloatProperty()
    datetime = ndb.DateTimeProperty()
    alt = ndb.FloatProperty()
    speed = ndb.FloatProperty()
    course = ndb.FloatProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)


class Update(webapp2.RequestHandler):
    def post(self):
        self.response.write('Updating location...****')
        location_name = self.request.get('location_name', LOCATION_NAME)
        location = Location(parent=location_key(location_name))
        location.lat = float(self.request.get("lat"))
        location.lng = float(self.request.get("long"))
        location.alt = float(self.request.get("alt"))
        location.datetime = datetime.strptime(self.request.get("datetime"), '%m/%d/%Y-%I/%M/%S/%f')
        date = self.request.get("datetime")
        location.speed = float(self.request.get("speed"))
        location.course = float(self.request.get("course"))
        self.response.write("%s %s %s" % (location.lat, location.lng, date))
        location.put()
        self.response.write('Location updated.')

class Current_Location(webapp2.RequestHandler):
    def get(self):
        location_query = Location.query(ancestor=location_key(LOCATION_NAME)).order(-Location.created)
        loc = location_query.fetch(1)
        if len(loc)!=0:
            now = datetime.now()
            timeist = loc[0].created + timedelta(hours = 5, minutes = 30)
            diff = now - loc[0].created
            allowed_diff = timedelta(minutes = 2)
            if diff > allowed_diff :
                elapsed_time = divmod(diff.total_seconds(), 60)
                connect_status = "The device is offline. Last Update was <b>%s Minutes and %s Seconds </b>Ago" % (int(elapsed_time[0]), int(elapsed_time[1]))
            else :
                elapsed_time = divmod(diff.total_seconds(), 60)
                connect_status = "The device is connected and updating location every 20 Seconds.Last location is from <b>%s Minutes and %s Seconds </b>Ago" % (int(elapsed_time[0]), int(elapsed_time[1]))
            map_url = 'https://maps.google.com/maps?q=%s,+%s&amp;ie=UTF8&amp;t=h&amp;z=19&amp;output=embed'% (loc[0].lat, loc[0].lng)
            self.response.write(PAGE_HEAD + "<body><center><h1>Tracker Position</h1><u>Last Updated<b> %s Minutes, %s Seconds ago </b><br>@ %s<br><br>"% (int(elapsed_time[0]), int(elapsed_time[1]), timeist.strftime('%a, %d, %b %Y at %I:%M:%S %p')))
            self.response.write('<iframe width="700" height="500" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="%s"></iframe>   <script src="http://code.jquery.com/jquery.js"></script><script src="http://localhost:9000/bootstrap/js/bootstrap.min.js"></script>' % (map_url))
            self.response.write('<br><b>Device Status</b>:%s </center></body></html>' % (connect_status))
        else:
            self.response.write('<h1>empty</h1>')

"""class Clean(webapp2.Requesthandler):
    def get(self):
        location_query = Location.query(ancestor=location_key(LOCATION_NAME)).order(Location.created)
        loc = location.query.fetch()


app = webapp2.WSGIApplication([
    ('/update', Update),
    ('/clean_data', Clean),
    ()
    ('/', Current_Location)
], debug=True)
