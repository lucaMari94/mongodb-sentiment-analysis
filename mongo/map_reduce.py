import pymongo
from bson import Code


client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

anger = db['anger']
anger_emoji = db['anger_emoji']
anger_emoticons = db['anger_emoticons']
anger_hashtag = db['anger_hashtag']

# Load map and reduce functions
map = Code(open('wordMap.js', 'r').read())
reduce = Code(open('wordReduce.js', 'r').read())

results = anger.map_reduce(map, reduce, "anger_frequency")
anger_emoji.map_reduce(map, reduce, "anger_emoji_frequency")
anger_emoticons.map_reduce(map, reduce, "anger_emoticons_frequency")
anger_hashtag.map_reduce(map, reduce, "anger_hashtag_frequency")

"""
anger_hashtag_frequency = db['anger_hashtag_frequency']
for x in anger_hashtag_frequency.find():
  print(x)"""
# Print the results
"""for result in results.find():
    print(result['_id'], result['value']['count'])"""

anger_emoticons_frequency = db['anger_emoticons_frequency']
anger_emoji_frequency = db['anger_emoji_frequency']
anger_hashtag_frequency = db['anger_hashtag_frequency']
anger_frequency = db['anger_frequency']

total = 0
for result in anger_emoticons_frequency.find():
    total += result['value']['count']
    # print(result['_id'], result['value']['count'])
print("total emotions = " + str(total))

total = 0
for result in anger_emoji_frequency.find():
    total += result['value']['count']
    # print(result['_id'], result['value']['count'])
print("total emoji = " + str(total))

total = 0
for result in anger_hashtag_frequency.find():
    total += result['value']['count']
    # print(result['_id'], result['value']['count'])
print("total hashtag = " + str(total))

total = 0
for result in anger_frequency.find():
    total += result['value']['count']
    # print(result['_id'], result['value']['count'])
print("total count anger = " + str(total))