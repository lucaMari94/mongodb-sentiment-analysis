import ast
import re
import mysql.connector

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

def insert_into_db(db, table_name, attribute_name, word, count):
    try:
        mycursor = db.cursor()
        sql = "INSERT INTO " + table_name + " (word, " + attribute_name + ") VALUES (%s, %s)"
        val = (word, count)
        mycursor.execute(sql, val)
        db.commit()
    except mysql.connector.Error as e:
        print(e)

def create_dict_perc(folder_name, emotion, file_name):

    # read file archive
    myfile = open("archive_risorse_lessicali/"+folder_name+"/"+file_name+".txt", "rt", encoding='utf-8')
    contents_arch = myfile.read()
    myfile.close()

    # read file result twitter
    myfile = open("result_count/"+emotion+"_global_dict_count.txt", "rt", encoding='utf-8')
    contents_twit = myfile.read()
    myfile.close()

    dict_twit = ast.literal_eval(contents_twit)

    dict_archive = {}

    words = []

    reg_expr = re.compile('[_]')

    for word in contents_arch.splitlines():

        # 1 Delete "_" from word
        if reg_expr.search(word) == None:
            words.append(word)

            # 2 Count presence in dict_twit
            if dict_twit.get(word)!=None:
                dict_archive[word] = dict_twit.get(word)

    # 3 total word in dict twit
    total_word_dict_twit = sum(dict_twit.values())
    print (total_word_dict_twit)
    dict_perc_word = {}

    for element in dict_archive:
        percentage_word = (dict_archive.get(element)/ total_word_dict_twit)*100

        dict_perc_word[element] = percentage_word

    return dict_perc_word

anger_emosn_dict_perc = create_dict_perc("Anger","anger","EmoSN_anger")
anger_nrc_dict_perc = create_dict_perc("Anger","anger","NRC_anger")
anger_sentisense_dict_perc = create_dict_perc("Anger","anger","sentisense_anger")

db = connect_to_db()

for element in anger_emosn_dict_perc:
    word = element
    count = anger_emosn_dict_perc.get(element)
    attribute_name = "emo_sn"
    table_name = "anger_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

for element in anger_nrc_dict_perc:
    word = element
    count = anger_emosn_dict_perc.get(element)
    attribute_name = "nrc"
    table_name = "anger_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

for element in anger_sentisense_dict_perc:
    word = element
    count = anger_emosn_dict_perc.get(element)
    attribute_name = "sentisense"
    table_name = "anger_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)