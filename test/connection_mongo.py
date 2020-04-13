from pymongo import MongoClient

# client
client = MongoClient('localhost', 27017)

# access to db
db = client.prova

# access to table
table = db.prova

post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"]
        }

post_id = table.insert_one(post).inserted_id

print(table.find_one({"author": "Mike"}))

# db.prova.deleteOne({"author": "Mike"})