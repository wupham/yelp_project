# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 18:34:09 2016

@author: Wesley
"""

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
insertQuery = "INSERT INTO yelp_categories (business_id, category) VALUES (%s, %s)"

with open('yelp_business.json') as myfile:
    for line in myfile:
        data = json.loads(line)
        businessID = data.get("business_id")
        categories = data.get("categories")
        if 'Restaurants' in categories:
            for category in categories:
                #print(businessID, category)
                cursorSelect.execute(insertQuery,(businessID, category))
            