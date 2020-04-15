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


def get_count_word_total():
    db = connect_to_db()
    try:
        mycursor = db.cursor()
        query = "SELECT SUM(frequency) from anger where (emo_sn = 1 or nrc = 1 or sentisense = 1)"
        mycursor.execute(query)
        return mycursor.fetchone()[0]
    except mysql.connector.Error as e:
        print(e)


count_total_anger = get_count_word_total()
print(count_total_anger)

anger_global_dict_count = get_result_count_dict('anger_global_dict_count')
total_word_dict_twit = sum(anger_global_dict_count.values())
print(total_word_dict_twit)

perc_anger = count_total_anger / total_word_dict_twit * 100
print(f"{perc_anger:.2f}")

# file = open("result_frequency/frequency.txt", "a", encoding='utf-8')
# file.write(json.dumps(global_dict_count))
# file.close()