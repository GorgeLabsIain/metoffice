# metoffice.py
from datetime import datetime
import sys
import json
import pymysql
import urllib.request

# get observation data from DataPoint API
url = "datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/"
site = "3414"
resolution = "hourly"
apikey = "afaf1e53-a676-4e25-a192-032d81e9a4e7"
datapoint = "http://" + url + site + "?res=" + resolution + "&key=" + apikey
data=json.load(urllib.request.urlopen(datapoint))

# read observation data from file
#data=json.load(open("observation_3414.json","r"))

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

# AWS RDS details
rds_host = "test-database.cvy5oxoofh9y.eu-west-2.rds.amazonaws.com"
name = "admin"
password = "eleksenadmin"
db_name = "test"
# connect to RDS instance
sqldb = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)

# get location_id from RDS
locaiton_id = []
with sqldb.cursor() as cursor:
    sql = "SELECT location_id FROM locations WHERE location_reference = %s"
    cursor.execute(sql, site)
    location_id = cursor.fetchall()

# send observation to RDS
with sqldb.cursor() as cursor:
    sql = "INSERT INTO weather (observation_id,location_id,observation_timestamp,observation_value,observation_type) VALUES (UNHEX(REPLACE(UUID(),'-','')), %s, %s, %s, %s)"
    cursor.execute(sql, (location_id[0], timestamp, temperature, "air temperature"))
    sqldb.commit()

# close connection to RDS
sqldb.close()