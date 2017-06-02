# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 15:28:59 2016

@author: wupham
"""
import nltk
#nltk.download()
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from collections import OrderedDict
from operator import itemgetter
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

#get information from the user requried for the problem
userHome = input("What city do you live in? ")
userState = input("What state do you live in (Abbreviation)? ")
userRes1 = input("List one of your favorite restaurants from this city: ")
userRes2 = input("List another of your favorite restaurants from this city: ")
userRes3 = input("List one more of your favorite restaurants from this city: ")
userNew1 = input("What city would you like recommendations for? ")
userNew2 = input("What state is this city located in? ")

#find the business id's and star rating for the inputted restaurants
cityQuery = "SELECT business_id, stars FROM yelp_business WHERE (name LIKE '" + userRes1 + "' or name LIKE '" + userRes2 + "' or name LIKE '" + userRes3 + "') AND (city LIKE '" + userHome + "' and State LIKE '" + userState + "')"
#find the avergae price range of the 3 inputted restaurants
priceQuery = "SELECT AVG(price_range) FROM yelp_business WHERE price_range IS NOT NULL AND (name LIKE '" + userRes1 + "' or name LIKE '" + userRes2 + "' or name LIKE '" + userRes3 + "') AND (city LIKE '" + userHome + "' and State LIKE '" + userState + "')"

#execute and fetch business id's and star ratings
cursorSelect.execute(cityQuery)
rows = cursorSelect.fetchall()

#set up empty string to hold reviews
textBlock = ''
#create variables
starAVG = 0
priceAVG = 0
#set up empty list to dump categories in
categoryList = []
print("analyzing restaurants...")

for row in rows:
    #get the business id
    businessID = row[0]
    #get the categories from this business
    categoryQuery = "SELECT category FROM yelp_categories WHERE business_id = '" + businessID + "'" 
    #execute and fetch the categories
    cursorSelect.execute(categoryQuery)
    categorys = cursorSelect.fetchall()
    #set up a loop to run through the categories, check if they are already in list and then put them in list
    for category in categorys:
        categoryClean = category[0]
        if categoryClean not in categoryList:
            categoryList.append(categoryClean)
    #get the star ratings for each business
    businessStar = row[1]
    #aggregate them so we can get the average later...
    starAVG = starAVG + businessStar
    #get the text from the reviews
    reviewQuery = "SELECT text from yelp_review WHERE business_id = '" + businessID + "'"
    #execute and fetch the results
    cursorSelect.execute(reviewQuery)
    reviews = cursorSelect.fetchall()
    #add each review to the blank string from before
    for texts in reviews:
        text = texts[0]
        textBlock = textBlock + text

#get the average star rating
starAVG = starAVG/3
#execute and fetch the average price of the inputted businesses        
cursorSelect.execute(priceQuery)
priceAVG = cursorSelect.fetchone()[0]

print("finding keywords from reviews...")   

#use nltk to find keywords from text block    
words = word_tokenize(textBlock)
lowercase_words = [word.lower() for word in words
                   if word not in stopwords.words() and word.isalpha()]
word_frequencies = FreqDist(lowercase_words)
most_frequent_words = FreqDist(lowercase_words).most_common(20)

# print out the keywords more nicely
for pair in most_frequent_words:
    print(pair[0],":",pair[1])

#convert average star and price to strings for queries
starAVG = str(starAVG)
priceAVG = str(priceAVG)

#set up query to pull out business that have a category from our list, and are greater than or equal to the average star rating of the users restaurants and less than or equal to the price range of the users restaurants
counter = 1
newQuery = "SELECT yelp_business.business_id FROM yelp_business INNER JOIN yelp_categories ON yelp_business.business_id = yelp_categories.business_id WHERE yelp_business.city LIKE '" + userNew1 + "' AND yelp_business.state LIKE '" + userNew2 + "' AND yelp_business.stars >= '" + starAVG + "' AND yelp_business.price_range <= '" + priceAVG + "' AND (yelp_categories.category = '" + categoryList[counter] + "'"

#using a loop to add each part of the category list to the query
counter += 1
while counter < len(categoryList):
    newQuery = newQuery + " OR yelp_categories.category = '" + categoryList[counter] + "'"
    counter += 1
#limiting results will decrease computing time, but also limit the options for our output
newQuery = newQuery + ") LIMIT 5"

#set up blank list of possible restaurants
possibleRestaurants = []

#execute the newQuery and fetch results 
cursorSelect.execute(newQuery)
restaurants = cursorSelect.fetchall()

#put the values in the possibleRestaurants list
for restaurant in restaurants:
    possibleRestaurants.append(restaurant[0])
print("finding new restaurants...")

#set up a dictionary to hold values of businesses and reviews
setRestaurants = {}

#loop through possible restaurants
for item in possibleRestaurants:
    #set up blank string to hold review text
    cleanReview = ''
    #run query for each restaurant
    getTextQuery = "SELECT business_id, text FROM yelp_review WHERE business_id = '" + item + "'"
    #execute and fetch results
    cursorSelect.execute(getTextQuery)
    listBusinessID = cursorSelect.fetchone()
    reviews = cursorSelect.fetchall()
    #put review in the blank string
    for review in reviews:
        cleanReview = cleanReview + review[1]
    #put businessID and review in dictionary
    setRestaurants[item] = cleanReview

#set up dictionary to begin ranking process
restaurantRank = {}

#go through first dictionary and see if any of my keywords are in that specfic review, if so add one to the counter. The one with the highest value will be ranked the highest and be the recommended restaurant.
for k, v in setRestaurants.items():
    counter = 0
    for word in most_frequent_words:
        if word[0] in v:
            counter += 1
    restaurantRank[k] = counter

print("ranking restaurant selection...")

#put the dictionary in a list to be able to sort it
ranks = restaurantRank.items()
sortedRanks = sorted(ranks, key=itemgetter(1), reverse=True)

#output the results
counter = 0
outputList = []
for place in sortedRanks:
    while counter < 4:
        restaurantID = place[0]
        outputQuery = "SELECT name FROM yelp_business WHERE business_id = '" + restaurantID + "'"
        cursorSelect.execute(outputQuery)
        outputRes = cursorSelect.fetchone()
        outputList.append(outputRes)
        counter += 1
    
print(outputList)
        
