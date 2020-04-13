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

def word_exist(db, table_name, word):
    try:
        mycursor = db.cursor()
        # SELECT * FROM `anger_percentage` WHERE word = "stir"
        query = 'SELECT * FROM `' + table_name + '` WHERE word = "' + word + '"'
        mycursor.execute(query)
        results = mycursor.fetchone()
        if results == None:
            return False
        else:
            return True

    except mysql.connector.Error as e:
        print(e)

def insert_into_db(db, table_name, attribute_name, word, count):
    try:
        mycursor = db.cursor()

        if word_exist(db, table_name, word):
            sql_update_query = "Update " + table_name + " set " + attribute_name + " = %s where word = %s"
            data = (count, word)
            mycursor.execute(sql_update_query, data)
            db.commit()
        else:
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


db = connect_to_db()

# anger
anger_emosn_dict_perc = create_dict_perc("Anger","anger","EmoSN_anger")
anger_nrc_dict_perc = create_dict_perc("Anger","anger","NRC_anger")
anger_sentisense_dict_perc = create_dict_perc("Anger","anger","sentisense_anger")

for element in anger_emosn_dict_perc:
    word = element
    count = anger_emosn_dict_perc.get(element)
    attribute_name = "emo_sn"
    table_name = "anger_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

for element in anger_nrc_dict_perc:
    word = element
    count = anger_nrc_dict_perc.get(element)
    attribute_name = "nrc"
    table_name = "anger_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

for element in anger_sentisense_dict_perc:
    word = element
    count = anger_sentisense_dict_perc.get(element)
    attribute_name = "sentisense"
    table_name = "anger_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

# anticipation

anticipation_nrc_dict_perc = create_dict_perc("Anticipation","anticipation","NRC_anticipation")
anticipation_sentisense_dict_perc = create_dict_perc("Anticipation","anticipation","sentisense_anticipation")

for element in anticipation_nrc_dict_perc:
    word = element
    count = anticipation_nrc_dict_perc.get(element)
    attribute_name = "nrc"
    table_name = "anticipation_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

for element in anticipation_sentisense_dict_perc:
    word = element
    count = anticipation_sentisense_dict_perc.get(element)
    attribute_name = "sentisense"
    table_name = "anticipation_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

# ConScore

# disgust-hate

# fear

fear_nrc_dict_perc = create_dict_perc("Fear","fear","NRC_fear")
fear_sentisense_dict_perc = create_dict_perc("Fear","fear","sentisense_fear")

for element in fear_nrc_dict_perc:
    word = element
    count = fear_nrc_dict_perc.get(element)
    attribute_name = "nrc"
    table_name = "fear_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

for element in fear_sentisense_dict_perc:
    word = element
    count = fear_sentisense_dict_perc.get(element)
    attribute_name = "sentisense"
    table_name = "fear_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

# hope

hope_sentisense_dict_perc = create_dict_perc("Hope","hope","sentisense_hope")

for element in hope_sentisense_dict_perc:
    word = element
    count = hope_sentisense_dict_perc.get(element)
    attribute_name = "sentisense"
    table_name = "hope_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

# joy
joy_emosn_dict_perc = create_dict_perc("Joy","joy","EmoSN_joy")
joy_nrc_dict_perc = create_dict_perc("Joy","joy","NRC_joy")
joy_sentisense_dict_perc = create_dict_perc("Joy","joy","sentisense_joy")

for element in joy_emosn_dict_perc:
    word = element
    count = joy_emosn_dict_perc.get(element)
    attribute_name = "emo_sn"
    table_name = "joy_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

for element in joy_nrc_dict_perc:
    word = element
    count = joy_nrc_dict_perc.get(element)
    attribute_name = "nrc"
    table_name = "joy_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

for element in joy_sentisense_dict_perc:
    word = element
    count = joy_sentisense_dict_perc.get(element)
    attribute_name = "sentisense"
    table_name = "joy_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

# like-love
# neg
# pos

# sadness

sadness_nrc_dict_perc = create_dict_perc("Sadness","sadness","NRC_sadness")
sadness_sentisense_dict_perc = create_dict_perc("Sadness","sadness","sentisense_sadness")

for element in sadness_nrc_dict_perc:
    word = element
    count = sadness_nrc_dict_perc.get(element)
    attribute_name = "nrc"
    table_name = "sadness_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

for element in sadness_sentisense_dict_perc:
    word = element
    count = sadness_sentisense_dict_perc.get(element)
    attribute_name = "sentisense"
    table_name = "sadness_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

# suprise

surprise_nrc_dict_perc = create_dict_perc("Suprise","suprise","NRC_suprise")
surprise_sentisense_dict_perc = create_dict_perc("Suprise","suprise","sentisense_suprise")

for element in surprise_nrc_dict_perc:
    word = element
    count = surprise_nrc_dict_perc.get(element)
    attribute_name = "nrc"
    table_name = "suprise_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

for element in surprise_sentisense_dict_perc:
    word = element
    count = surprise_sentisense_dict_perc.get(element)
    attribute_name = "sentisense"
    table_name = "suprise_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)

# trust

trust_nrc_dict_perc = create_dict_perc("Trust","trust","NRC_trust")

for element in trust_nrc_dict_perc:
    word = element
    count = trust_nrc_dict_perc.get(element)
    attribute_name = "nrc"
    table_name = "trust_percentage"
    insert_into_db(db, table_name, attribute_name, word, count)