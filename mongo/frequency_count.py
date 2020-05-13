import pymongo


def get_perc(collection):
    frequency_collection = db[collection]

    total_resource_lexical = 0
    total = 0
    for record in frequency_collection.find():
        total += record['value']['count']
        if record['lexical_resources']:
            if {'EmoSN':1} in record['lexical_resources'] or {'NRC':1} in record['lexical_resources'] or {'SentiSense':1} in record['lexical_resources']:
                total_resource_lexical += record['value']['count']

    perc_emotion = total_resource_lexical / total * 100

    return f"{perc_emotion:.2f}"


client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

arr_emotions = ["anger_frequency", "anticipation_frequency", "disgust_frequency", "fear_frequency", "joy_frequency", "sadness_frequency", "surprise_frequency", "trust_frequency"]

file = open("frequency.txt", "w", encoding='utf-8')

total = 0
for emotion in arr_emotions:
    perc_count = get_perc(emotion)
    total += float(perc_count)
    text = emotion+": "+perc_count+"\n"
    file.write(text)

media = (float(total)/8)
media = f"{media:.2f}"
file.write("media = " + str(media))
file.close()