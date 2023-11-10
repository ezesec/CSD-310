""" 
    Title: mongodb_test.py
    Author: Ebenezer Evanoff
    Date: 11 November 2023
    Description: Test program for connecting to a 
                 MongoDB Atlas cluster
"""

""" import statements """
from pymongo import MongoClient

# MongoDB connection string 
url = "mongodb+srv://admin:admin@cluster0.oxzqyoe.mongodb.net/?retryWrites=true&w=majority"

# connect to the MongoDB cluster 
client = MongoClient(url)

# connect pytech database
db = client.pytech

# show the connected collections 
print("\n -- Pytech Collection List --")
print(db.list_collection_names())

# show an exit message
input("\n\n  End of program, press any key to exit... ")