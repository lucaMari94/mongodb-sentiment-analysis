import mysql.connector
import ast

# read from file
def load_emotion_from_dict(emotion):
    myfile = open("result_count/global_dict_count_" + emotion, "rt", encoding='utf-8')
    dict = myfile.read()
    myfile.close()
    return dict

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

def insert_into_db(emotion, db, element, dict):
    try:
        mycursor = db.cursor()
        sql = "INSERT INTO " + emotion + " (word, count) VALUES (%s, %s)"
        val = (element, dict[element])
        mycursor.execute(sql, val)
        db.commit()
    except mysql.connector.Error as e:
        print(e)

db = connect_to_db()

dataset_sentiment = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

for emotion in dataset_sentiment:
    string_dict = load_emotion_from_dict(emotion)
    # trasform string to dictionary
    dict = ast.literal_eval(string_dict)
    for element in dict:
        # print(element)
        # print(dict[element])
        insert_into_db(emotion, db, element, dict)