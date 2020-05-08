import pymongo

client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

dataset_sentiment = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

for emotion in dataset_sentiment:

    emotion_word = db[emotion + '_word']

    myquery = {"word": "get"}
    myquery = {"word": "go"}
    myquery = {"word": "i'm"}

    emotion_word.delete_one(myquery)