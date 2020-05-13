import pymongo

client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

anger_frequency_collection = db["anger_frequency"]

anger_frequency_collection.aggregate([{
    "$group": {
        "total": {
            "$sum": "$count"
        }
    }
}])