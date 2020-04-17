from pymongo import MongoClient
from bson.code import Code

# http://aimotion.blogspot.com/2010/08/mapreduce-with-mongodb-and-python.html


# client
connection = MongoClient('localhost', 27017)
db = connection.test

# insert data
# myfile = open("words.txt", "rt", encoding='utf-8')
myfile = open("../twitter_message/dataset_dt_" + "anger" + "_60k.txt", "rt", encoding='utf-8')
lines = myfile.read()
myfile.close()

[db.texts.insert_one({'word': word}) for word in lines.split()]


# load map and reduce functions
map = Code(open('wordMap.js', 'r').read())
reduce = Code(open('wordReduce.js', 'r').read())

# run the map-reduce query
results = db.texts.map_reduce(map, reduce, "output")

for result in results.find():
    print(result['_id'], result['value']['count'])

