# metoffice.py
from datetime import datetime
import sys
import json
import urllib.request

# get observation data from DataPoint API
#url = "datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/"
#site = "3414"
#resolution = "hourly"
#apikey = "afaf1e53-a676-4e25-a192-032d81e9a4e7"
#datapoint = "http://" + url + site + "?res=" + resolution + "&key=" + apikey
#data=json.load(urllib.request.urlopen(datapoint))

# read observation data from file
data=json.load(open("observation_3414.json","r"))

# get weather station details
name = data['SiteRep']['DV']['Location']['name']
latitude = data['SiteRep']['DV']['Location']['lat']
longitude = data['SiteRep']['DV']['Location']['lon']
elevation = data['SiteRep']['DV']['Location']['elevation']
print(name.capitalize())
print(latitude, longitude, elevation)

# get observation timestamp
day = data['SiteRep']['DV']['Location']['Period'][-1]['value']
hours = str(len(data['SiteRep']['DV']['Location']['Period'][-1]['Rep'])-1)
timestamp = datetime.strptime(day+hours, "%Y-%m-%dZ%H")
print(timestamp)

# get temperature reading
temperature = data['SiteRep']['DV']['Location']['Period'][-1]['Rep'][-1]['T']
print(temperature)
