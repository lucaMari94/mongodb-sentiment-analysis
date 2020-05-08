import pymongo
from bson import Code


client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

dataset_sentiment = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

for emotion in dataset_sentiment:

    emotion_word = db[emotion + '_word']
    emotion_emoji = db[emotion + '_emoji']
    emotion_emoticons = db[emotion + '_emoticons']
    emotion_hashtag = db[emotion +'_hashtag']

    # Load map and reduce functions
    map = Code(open('wordMap.js', 'r').read())
    reduce = Code(open('wordReduce.js', 'r').read())

    results = emotion_word.map_reduce(map, reduce, emotion + "_frequency")
    emotion_emoji.map_reduce(map, reduce, emotion + "_emoji_frequency")
    emotion_emoticons.map_reduce(map, reduce, emotion + "_emoticons_frequency")
    emotion_hashtag.map_reduce(map, reduce, emotion + "_hashtag_frequency")