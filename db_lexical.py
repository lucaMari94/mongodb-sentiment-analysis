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


# anger
# emosn, nrc, sentisense
dict_attribute_boolean = {"EmoSN_anger.txt" : 'emo_sn',
    "NRC_anger.txt" : 'nrc',
    "sentisense_anger.txt" : 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Anger", element)
    update_db(dict_lexical_archive, 'anger', dict_attribute_boolean.get(element), 'anger_global_dict_count')


# con score
# key = filename, value = attributename
dict_file = {"afinn.txt" : "afinn",
    "anewAro_tab.tsv" : "anew_aro",
    "anewDom_tab.tsv" : "anew_dom",
    "anewPleas_tab.tsv" : "anew_pleas",
    "Dal_Activ.csv" : "dal_activ",
    "Dal_imag.csv" : "dal_imag",
    "Dal_Pleas.csv" : "dal_pleas"}

for element in dict_file:
    dict = {}
    dict.clear()
    dict_con_score = {}
    dict_con_score.clear()
    dict = get_lexical_archive("ConScore", element)
    dict_con_score = get_lexical_archive_con_score(dict)
    update_db_con_score(dict_con_score, "anger", dict_file.get(element), "anger_global_dict_count")