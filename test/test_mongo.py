import pymongo

client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['test']

collection = db['cities']

mylist = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Hannah", "address": "Mountain 21"},
  { "name": "Michael", "address": "Valley 345"},
  { "name": "Sandy", "address": "Ocean blvd 2"},
  { "name": "Betty", "address": "Green Grass 1"},
  { "name": "Richard", "address": "Sky st 331"},
  { "name": "Susan", "address": "One way 98"},
  { "name": "Vicky", "address": "Yellow Garden 2"},
  { "name": "Ben", "address": "Park Lane 38"},
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"},
  { "name": "Prova1", "address": "Apple st 652"},
  { "name": "Prova2", "address": "Mountain 21"},
  { "name": "Prova3", "address": "Valley 345"},
  { "name": "Prova3", "address": "Ocean blvd 2"},
  { "name": "Prova4", "address": "Green Grass 1"},
  { "name": "Prova5", "address": "Sky st 331"},
  { "name": "Prova6", "address": "One way 98"},
  { "name": "Prova7", "address": "Yellow Garden 2"},
  { "name": "Prova8", "address": "Park Lane 38"},
  { "name": "Prova9", "address": "Central st 954"},
  { "name": "Prova10", "address": "Main Road 989"},
  { "name": "Prova11", "address": "Sideway 1633"}
]

collection.insert_many(mylist)

i = 0
for x in collection.find():
    i = i + 1
    print(x)

print(i)