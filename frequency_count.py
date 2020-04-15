import json

import mysql.connector
import ast


def connect_to_db():
    try:
        db = mysql.connector.connect(
          host="localhost",
          user="emotion",
          passwd="emotion",
          database="emotion"
        )
        return db
    except mysql.connector.Error as e:
        print(e)


def get_result_count_dict(result_count_dict):
    myfile = open("result_count/"+ result_count_dict +".txt", "rt", encoding='utf-8')
    contents_twit = myfile.read()
    myfile.close()
    return ast.literal_eval(contents_twit)


def get_count_word_total(table_name):
    db = connect_to_db()
    try:
        mycursor = db.cursor()
        query = "SELECT SUM(frequency) from "+table_name+" where (emo_sn = 1 or nrc = 1 or sentisense = 1)"
        mycursor.execute(query)
        return mycursor.fetchone()[0]
    except mysql.connector.Error as e:
        print(e)


def perc_lexical_into_twitter_msg(emotion):

    count_total_emotion = get_count_word_total(emotion)

    emotion_global_dict_count = get_result_count_dict(emotion+'_global_dict_count')
    total_word_dict_twit = sum(emotion_global_dict_count.values())

    perc_emotion = count_total_emotion/ total_word_dict_twit * 100

    return f"{perc_emotion:.2f}"

arr_emotions = ["anger","anticipation","disgust","fear","joy","sadness","surprise","trust"]

file = open("result_frequency/frequency.txt", "a", encoding='utf-8')

for emotion in arr_emotions:
    perc_count = perc_lexical_into_twitter_msg(emotion)
    file.write(json.dumps(perc_count))

file.close()