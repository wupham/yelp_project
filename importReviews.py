# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
insertQuery = "INSERT INTO yelp_review (review_id, type, business_id, user_id, stars, text, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"

yelpList = []
counter = 0
with open('yelp_academic_dataset_review.json') as myfile:
    for line in myfile:
        data = json.loads(line)
        yelpType = data.get("type")
        businessID = data.get("business_id")
        userID = data.get("user_id")
        stars = data.get("stars")
        text = data.get("text")
        date = data.get("date")
        cleanText = text.replace('\t',' ').replace('\n',' ').replace('\r',' ')
        counter = counter + 1
        cursorSelect.execute(insertQuery,(counter, yelpType, businessID, userID, stars, cleanText, date))
        
