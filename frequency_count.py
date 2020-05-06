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

    if table_name == 'anger':
        query = "SELECT SUM(frequency) from " + table_name + " where (emo_sn = 1 or nrc = 1 or sentisense = 1)"
    elif table_name == 'anticipation':
        query = "SELECT SUM(frequency) from " + table_name + " where (nrc = 1 or sentisense = 1)"
    elif table_name == 'disgust':
        query = "SELECT SUM(frequency) from " + table_name + " where (nrc = 1 or sentisense_disgust = 1 " \
                                                             "or sentisense_hate = 1)"
    elif table_name == 'fear':
        query = "SELECT SUM(frequency) from " + table_name + " where (nrc = 1 or sentisense = 1)"
    elif table_name == 'joy':
        query = "SELECT SUM(frequency) from " + table_name + " where (emo_sn = 1 or nrc = 1 or sentisense = 1)"
    elif table_name == 'sadness':
        query = "SELECT SUM(frequency) from " + table_name + " where (nrc = 1 or sentisense = 1)"
    elif table_name == 'surprise':
        query = "SELECT SUM(frequency) from " + table_name + " where (nrc = 1 or sentisense = 1)"
    elif table_name == 'trust':
        query = "SELECT SUM(frequency) from " + table_name + " where (nrc = 1)"

    db = connect_to_db()
    try:
        mycursor = db.cursor()
        mycursor.execute(query)
        return mycursor.fetchone()[0]
    except mysql.connector.Error as e:
        print(e)


def perc_lexical_into_twitter_msg(emotion):

    count_total_emotion = get_count_word_total(emotion)
    emotion_global_dict_count = get_result_count_dict(emotion+'_global_dict_count')
    total_word_dict_twit = sum(emotion_global_dict_count.values())

    perc_emotion = count_total_emotion/total_word_dict_twit * 100

    return f"{perc_emotion:.2f}"


arr_emotions = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

file = open("frequency.txt", "w", encoding='utf-8')

total = 0
for emotion in arr_emotions:
    perc_count = perc_lexical_into_twitter_msg(emotion)
    total += float(perc_count)
    text = emotion+": "+perc_count+"\n"
    file.write(text)

media = (float(total)/8)
media = f"{media:.2f}"
file.write("media = " + str(media))
file.close()