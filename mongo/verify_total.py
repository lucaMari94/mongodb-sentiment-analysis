import pymongo

client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

dataset_sentiment = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

for emotion in dataset_sentiment:
    emotion_emoticons_frequency = db[emotion + '_emoticons_frequency']
    emotion_emoji_frequency = db[emotion +'_emoji_frequency']
    emotion_hashtag_frequency = db['anger_hashtag_frequency']
    emotion_frequency = db['anger_frequency']

    # emotions
    print(emotion)
    print("emoticons")
    total = 0
    for result in emotion_emoticons_frequency.find():
        total += result['value']['count']
    print("total emotions = " + str(total))

    print("-")

    print("emoji")
    total = 0
    for result in emotion_emoji_frequency.find():
        total += result['value']['count']
    print("total emoji = " + str(total))

    print("-")

    print("hashtag")
    total = 0
    for result in emotion_hashtag_frequency.find():
        total += result['value']['count']
    print("total hashtag = " + str(total))

    print("-")

    print("words")
    total = 0
    for result in emotion_frequency.find():
        total += result['value']['count']
    print("total count anger = " + str(total))

    print("----------------------------------------------")