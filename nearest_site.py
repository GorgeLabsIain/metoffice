import pymysql
import json
import math

# base location
latitude = 52.595484
longitude = -1.213936

# AWS RDS details
rds_host = "test-database.cvy5oxoofh9y.eu-west-2.rds.amazonaws.com"
name = "admin"
password = "eleksenadmin"
db_name = "test"
# connect to RDS instance
sqldb = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)

# get locations from RDS
with sqldb.cursor() as cursor:
    sql = "SELECT location_latitude,location_longitude,location_id,location_name FROM locations"
    cursor.execute(sql, )
    data = cursor.fetchall()

    distance = []
    for location in data:
        # calculate distance to location
        lat = location[0]
        lon = location[1]
        distance.append((math.sqrt((latitude-lat)**2 + (longitude-lon)**2),location[2],location[3]))
    # sort list of distances
    distance.sort()
    print(distance[0])

# close connection to RDS
sqldb.close()
