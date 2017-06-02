# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 18:55:35 2016

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
insertQuery = "INSERT INTO yelp_business_categories (category_id, category) VALUES (%s, %s)"

categoryList = []

with open('yelp_business.json') as myfile:
    for line in myfile:
        data = json.loads(line)
        categories = data.get("categories")
        if 'Restaurants' in categories:
            for category in categories:
                if category not in categoryList:
                    categoryList.append(category)
                  
counter = 0
for item in categoryList:
    counter = counter + 1
    cursorSelect.execute(insertQuery,(counter, item))
