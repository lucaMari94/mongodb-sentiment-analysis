import pymongo

client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

anger_word_collection = db["anticipation_frequency"]

for x in anger_word_collection.find({"_id": "sit"}):
    print(x)