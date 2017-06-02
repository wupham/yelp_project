# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 12:54:34 2016

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
updateQuery = "UPDATE yelp_business SET price_range = %s WHERE business_id = %s"

with open('yelp_business.json') as myfile:
    for line in myfile:
        data = json.loads(line)
        price = data.get("attributes")
        businessID = data.get("business_id")
        priceRange = price.get("Price Range")
        #print(priceRange, businessID)
        cursorSelect.execute(updateQuery,(priceRange, businessID))