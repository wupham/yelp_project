# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 18:14:42 2016

@author: Wesley
"""

import json
import pymysql
import sys

#grab password from commandline 
password = sys.argv[1]

# Open database connection
db = pymysql.connect(host='cs.elon.edu',
                     db='wupham',
                     user='wupham',
                     passwd=password,
                     port=3306,
                     charset='utf8mb4',
                     autocommit=True)

cursorSelect = db.cursor()
insertQuery = "INSERT INTO yelp_business (business_id, type, name, city, state, latitude, longitude, stars) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

with open('yelp_business.json') as myfile:
    for line in myfile:
        data = json.loads(line)
        busType = data.get("type")
        businessID = data.get("business_id")
        name = data.get("name")
        city = data.get("city")
        state = data.get("state")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        stars = data.get("stars")
        #print(busType, businessID, name, city, state, latitude, longitude, stars)
        cursorSelect.execute(insertQuery,(businessID, busType, name, city, state, latitude, longitude, stars))
        