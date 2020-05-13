import pymongo

client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['test']

collection = db["prova"]

result = collection.update_one(
    {"company":"Capital One"},
    # {"$set": {"30L": [1,2,3,4,5]}},
    {"$set": {"lexical_resources": []}}
)

i = 0
while i < 10:
    result = collection.update_one(
        {"company": "Capital One"},
        {"$push": {"lexical_resources": {"EmoSN_"+str(i): i }}}
    )
    i = i + 1
