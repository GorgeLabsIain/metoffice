import pymysql

# AWS Aurora details
rds_host = "eleksen.cluster-cvy5oxoofh9y.eu-west-2.rds.amazonaws.com"
name = "admin"
password = "eleksenadmin"
db_name = "eleksen"
# connect to RDS instance
print("Connecting to Aurora")
sqldb = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=60)

# create Aurora database
print("Creating database")
with sqldb.cursor() as cursor:
    sql = "CREATE DATABASE IF NOT EXISTS eleksen"
    cursor.execute(sql, )
    sqldb.commit()
    print("done")

# create database table
print("Creating table: locations")
with sqldb.cursor() as cursor:
    sql = "CREATE TABLE IF NOT EXISTS locations (location_id BINARY(16) NOT NULL,location_name VARCHAR(255) NOT NULL,location_latitude FLOAT,location_longitude FLOAT,location_elevation FLOAT,location_reference VARCHAR(255),PRIMARY KEY(location_id),UNIQUE INDEX(location_name));"
    cursor.execute(sql, )
    sqldb.commit()
    print("done")

# create database table
print("Creating table: weather")
with sqldb.cursor() as cursor:
    sql = "CREATE TABLE IF NOT EXISTS weather (observation_id BINARY(16) NOT NULL,location_id BINARY(16) NOT NULL,observation_timestamp TIMESTAMP,observation_value FLOAT,observation_type ENUM ('air temperature','air pressure','wind speed','wind direction','wind gust','visibility','dew point'),PRIMARY KEY (observation_id));"
    cursor.execute(sql, )
    sqldb.commit()
    print("done")

# close connection to RDS
sqldb.close()
print("Disconnected from Aurora")
