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


def get_lexical_archive(foldername, filename):
    # read file archive
    myfile = open("archive_risorse_lessicali/"+ foldername + "/" + filename, "rt", encoding='utf-8')
    contents_arch = myfile.read()
    myfile.close()
    words = []
    reg_expr = re.compile('[_]')
    # 1 Delete "_" from word (archive)
    for word in contents_arch.splitlines():
        # 1 Delete "_" from word
        if reg_expr.search(word) == None:
            words.append(word)
    return words


def get_lexical_archive_con_score(dict):

    dict_con_score = {}

    for element in dict:
        array = element.split("\t")
        dict_con_score[array[0]] = array[1]

    return dict_con_score


def get_result_count_dict(result_count_dict):
    myfile = open("result_count/"+ result_count_dict +".txt", "rt", encoding='utf-8')
    contents_twit = myfile.read()
    myfile.close()
    return ast.literal_eval(contents_twit)


# for boolean attribute : set 1 if present in dictionary twitter
def update_db(words, table_name, attributename, result_count_dict):
    # read file dictionary
    dict_twit = get_result_count_dict(result_count_dict)

    db = connect_to_db()

    # tweet dictionary
    for element in dict_twit:
        if element in words:
            try:
                # print(element)
                mycursor = db.cursor()
                query = "Update " + table_name + " set " + attributename + " = %s where word = %s"
                data = (1, element)
                mycursor.execute(query, data)
                db.commit()
            except mysql.connector.Error as e:
                print(e)


def update_db_con_score(dict, table_name, attributename, result_count_dict):
    # read file dictionary
    dict_twit = get_result_count_dict(result_count_dict)

    db = connect_to_db()
    for element in dict_twit:
        if element in dict:
            try:
                # print(element)
                mycursor = db.cursor()
                query = "Update " + table_name + " set " + attributename + " = %s where word = %s"
                data = (dict.get(element), element)
                mycursor.execute(query, data)
                db.commit()
            except mysql.connector.Error as e:
                print(e)


# key = filename, value = attributename
global_con_score = {"afinn.txt" : "afinn",
    "anewAro_tab.tsv" : "anew_aro",
    "anewDom_tab.tsv" : "anew_dom",
    "anewPleas_tab.tsv" : "anew_pleas",
    "Dal_Activ.csv" : "dal_activ",
    "Dal_imag.csv" : "dal_imag",
    "Dal_Pleas.csv" : "dal_pleas"}

dict_attribute_neg = {"GI_NEG.txt": "gi_neg",
                          "HL-negatives.txt": "hl_neg",
                          "listNegEffTerms.txt": "list_neg",
                          "LIWC-NEG.txt": "liwc_neg"}

dict_attribute_pos = {"GI_POS.txt": "gi_pos",
                          "HL-positives.txt": "hl_pos",
                          "listPosEffTerms.txt": "list_pos",
                          "LIWC-POS.txt": "liwc_pos"}

#############################################################################
# anger

dict_attribute_boolean = {"EmoSN_anger.txt" : 'emo_sn',
    "NRC_anger.txt" : 'nrc',
    "sentisense_anger.txt" : 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Anger", element)
    update_db(dict_lexical_archive, 'anger', dict_attribute_boolean.get(element), 'anger_global_dict_count')

for element in dict_attribute_neg:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Neg", element)
    update_db(dict_lexical_archive, 'anger', dict_attribute_neg.get(element), 'anger_global_dict_count')

for element in dict_attribute_pos:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Pos", element)
    update_db(dict_lexical_archive, 'anger', dict_attribute_pos.get(element), 'anger_global_dict_count')


# anger con score
for element in global_con_score:
    dict = {}
    dict.clear()
    dict_con_score = {}
    dict_con_score.clear()
    dict = get_lexical_archive("ConScore", element)
    dict_con_score = get_lexical_archive_con_score(dict)
    update_db_con_score(dict_con_score, "anger", global_con_score.get(element), "anger_global_dict_count")

#############################################################################
# anticipation


# dict_attribute_boolean.clear()

dict_attribute_boolean = {"NRC_anticipation.txt" : 'nrc',
    "sentisense_anticipation.txt" : 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Anticipation", element)
    update_db(dict_lexical_archive, 'anticipation', dict_attribute_boolean.get(element), 'anticipation_global_dict_count')

for element in dict_attribute_neg:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Neg", element)
    update_db(dict_lexical_archive, 'anticipation', dict_attribute_neg.get(element), 'anticipation_global_dict_count')

for element in dict_attribute_pos:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Pos", element)
    update_db(dict_lexical_archive, 'anticipation', dict_attribute_pos.get(element), 'anticipation_global_dict_count')

# con score
# key = filename, value = attributename

for element in global_con_score:
    dict = {}
    dict.clear()
    dict_con_score = {}
    dict_con_score.clear()
    dict = get_lexical_archive("ConScore", element)
    dict_con_score = get_lexical_archive_con_score(dict)
    update_db_con_score(dict_con_score, "anticipation", global_con_score.get(element), "anticipation_global_dict_count")


#############################################################################
# disgust-hate

dict_attribute_boolean.clear()

dict_attribute_boolean = {"NRC_disgust.txt" : 'nrc',
    "sentisense_disgust.txt" : 'sentisense_disgust',
    "sentisense_hate.txt" : 'sentisense_hate'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Disgust-Hate", element)
    update_db(dict_lexical_archive, 'disgust', dict_attribute_boolean.get(element), 'disgust_global_dict_count')

for element in dict_attribute_neg:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Neg", element)
    update_db(dict_lexical_archive, 'disgust', dict_attribute_neg.get(element), 'disgust_global_dict_count')

for element in dict_attribute_pos:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Pos", element)
    update_db(dict_lexical_archive, 'disgust', dict_attribute_pos.get(element), 'disgust_global_dict_count')

# con score
# key = filename, value = attributename

for element in global_con_score:
    dict = {}
    dict.clear()
    dict_con_score = {}
    dict_con_score.clear()
    dict = get_lexical_archive("ConScore", element)
    dict_con_score = get_lexical_archive_con_score(dict)
    update_db_con_score(dict_con_score, "disgust", global_con_score.get(element), "disgust_global_dict_count")


#############################################################################
# fear

dict_attribute_boolean.clear()

dict_attribute_boolean = {"NRC_fear.txt" : 'nrc',
    "sentisense_fear.txt" : 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Fear", element)
    update_db(dict_lexical_archive, 'fear', dict_attribute_boolean.get(element), 'fear_global_dict_count')

for element in dict_attribute_neg:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Neg", element)
    update_db(dict_lexical_archive, 'fear', dict_attribute_neg.get(element), 'fear_global_dict_count')

for element in dict_attribute_pos:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Pos", element)
    update_db(dict_lexical_archive, 'fear', dict_attribute_pos.get(element), 'fear_global_dict_count')

# con score
# key = filename, value = attributename

for element in global_con_score:
    dict = {}
    dict.clear()
    dict_con_score = {}
    dict_con_score.clear()
    dict = get_lexical_archive("ConScore", element)
    dict_con_score = get_lexical_archive_con_score(dict)
    update_db_con_score(dict_con_score, "fear", global_con_score.get(element), "fear_global_dict_count")


#############################################################################
# Joy

dict_attribute_boolean.clear()

dict_attribute_boolean = {"EmoSN_joy.txt": 'emo_sn',
    "NRC_joy.txt" : 'nrc',
    "sentisense_joy.txt" : 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Joy", element)
    update_db(dict_lexical_archive, 'joy', dict_attribute_boolean.get(element), 'joy_global_dict_count')

for element in dict_attribute_neg:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Neg", element)
    update_db(dict_lexical_archive, 'joy', dict_attribute_neg.get(element), 'joy_global_dict_count')

for element in dict_attribute_pos:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Pos", element)
    update_db(dict_lexical_archive, 'joy', dict_attribute_pos.get(element), 'joy_global_dict_count')

# con score
# key = filename, value = attributename

for element in global_con_score:
    dict = {}
    dict.clear()
    dict_con_score = {}
    dict_con_score.clear()
    dict = get_lexical_archive("ConScore", element)
    dict_con_score = get_lexical_archive_con_score(dict)
    update_db_con_score(dict_con_score, "joy", global_con_score.get(element), "joy_global_dict_count")


#############################################################################
# Sadness

dict_attribute_boolean.clear()

dict_attribute_boolean = {"NRC_sadness.txt": 'nrc',
                          "sentisense_sadness.txt": 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Sadness", element)
    update_db(dict_lexical_archive, 'sadness', dict_attribute_boolean.get(element), 'sadness_global_dict_count')

for element in dict_attribute_neg:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Neg", element)
    update_db(dict_lexical_archive, 'sadness', dict_attribute_neg.get(element), 'sadness_global_dict_count')

for element in dict_attribute_pos:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Pos", element)
    update_db(dict_lexical_archive, 'sadness', dict_attribute_pos.get(element), 'sadness_global_dict_count')

# con score
# key = filename, value = attributename

for element in global_con_score:
    dict = {}
    dict.clear()
    dict_con_score = {}
    dict_con_score.clear()
    dict = get_lexical_archive("ConScore", element)
    dict_con_score = get_lexical_archive_con_score(dict)
    update_db_con_score(dict_con_score, "sadness", global_con_score.get(element), "sadness_global_dict_count")


#############################################################################
# Surprise

# dict_attribute_boolean.clear()

dict_attribute_boolean = {"NRC_surprise.txt": 'nrc',
                          "sentisense_surprise.txt": 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Surprise", element)
    update_db(dict_lexical_archive, 'surprise', dict_attribute_boolean.get(element), 'surprise_global_dict_count')

for element in dict_attribute_neg:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Neg", element)
    update_db(dict_lexical_archive, 'surprise', dict_attribute_neg.get(element), 'surprise_global_dict_count')

for element in dict_attribute_pos:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Pos", element)
    update_db(dict_lexical_archive, 'surprise', dict_attribute_pos.get(element), 'surprise_global_dict_count')

# con score
# key = filename, value = attributename

for element in global_con_score:
    dict = {}
    dict.clear()
    dict_con_score = {}
    dict_con_score.clear()
    dict = get_lexical_archive("ConScore", element)
    dict_con_score = get_lexical_archive_con_score(dict)
    update_db_con_score(dict_con_score, "surprise", global_con_score.get(element), "surprise_global_dict_count")


#############################################################################
# Trust

dict_attribute_boolean.clear()

dict_attribute_boolean = {"NRC_trust.txt": 'nrc'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Trust", element)
    update_db(dict_lexical_archive, 'trust', dict_attribute_boolean.get(element), 'trust_global_dict_count')

for element in dict_attribute_neg:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Neg", element)
    update_db(dict_lexical_archive, 'trust', dict_attribute_neg.get(element), 'trust_global_dict_count')

for element in dict_attribute_pos:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Pos", element)
    update_db(dict_lexical_archive, 'trust', dict_attribute_pos.get(element), 'trust_global_dict_count')

# con score
# key = filename, value = attributename

for element in global_con_score:
    dict = {}
    dict.clear()
    dict_con_score = {}
    dict_con_score.clear()
    dict = get_lexical_archive("ConScore", element)
    dict_con_score = get_lexical_archive_con_score(dict)
    update_db_con_score(dict_con_score, "trust", global_con_score.get(element), "trust_global_dict_count")