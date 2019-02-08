import json
import pymysql
import sys
import urllib.request

# get observation site list from DataPoint API
url = "datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/sitelist"
apikey = "afaf1e53-a676-4e25-a192-032d81e9a4e7"
datapoint = "http://" + url + "?key=" + apikey
print(datapoint)
data=json.load(urllib.request.urlopen(datapoint))

# read observation site list from file
#data=json.load(open("observation_sitelist.json","r"))

locations=data['Locations']['Location']
print(len(locations))

# AWS RDS details
rds_host = "test-database.cvy5oxoofh9y.eu-west-2.rds.amazonaws.com"
name = "admin"
password = "eleksenadmin"
db_name = "test"
# connect to RDS instance
sqldb = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)

# iterate for each location
for location in locations:
    # get location
    loc=location['name']
    lat=location['latitude']
    lon=location['longitude']
    ele=location['elevation']
    ref=location['id']
    print(loc)

    # send location to RDS
    with sqldb.cursor() as cursor:
        sql = "INSERT INTO locations (location_id,location_name,location_latitude,location_longitude,location_elevation,location_reference) VALUES (UNHEX(REPLACE(UUID(),'-','')), %s, %s, %s, %s, %s)"
        cursor.execute(sql, (loc, lat, lon, ele, ref))
        sqldb.commit()

# close connection to RDS
sqldb.close()
