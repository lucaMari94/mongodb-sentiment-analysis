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

"""
anger_emosn = get_lexical_archive("Anger", "EmoSN_anger.txt")
update_db(anger_emosn, 'anger', 'emo_sn', 'anger_global_dict_count')

anger_nrc = get_lexical_archive("Anger", "NRC_anger.txt")
update_db(anger_nrc, 'anger', 'nrc', 'anger_global_dict_count')

anger_sentisense = get_lexical_archive("Anger", "sentisense_anger.txt")
update_db(anger_sentisense, 'anger', 'sentisense', 'anger_global_dict_count')


dict_twit = get_result_count_dict("anger_global_dict_count")
"""

list_file= ["afinn.txt","anewAro_tab.tsv","anewDom_tab.tsv",
            "anewPleas_tab.tsv","Dal_Activ.csv","Dal_imag.csv",
            "Dal_Pleas.csv"]


anger_afinn = get_lexical_archive("ConScore", "afinn.txt")
dict_afinn = get_lexical_archive_con_score(anger_afinn)
update_db_con_score(dict_afinn,"anger","afinn","anger_global_dict_count")


anger_anew_aro = get_lexical_archive("ConScore", "anewAro_tab.tsv")
dict_anew_aro = get_lexical_archive_con_score(anger_anew_aro)
update_db_con_score(dict_anew_aro,"anger","anew_aro","anger_global_dict_count")

anger_anew_dom = get_lexical_archive("ConScore", "anewDom_tab.tsv")
dict_anew_dom = get_lexical_archive_con_score(anger_anew_dom)
update_db_con_score(dict_anew_dom,"anger","anew_dom","anger_global_dict_count")

anger_anew_pleas = get_lexical_archive("ConScore", "anewPleas_tab.tsv")
dict_anew_pleas = get_lexical_archive_con_score(anger_anew_pleas)
update_db_con_score(dict_anew_pleas,"anger","anew_pleas","anger_global_dict_count")

anger_dal_active = get_lexical_archive("ConScore", "Dal_Activ.csv")
dict_dal_active = get_lexical_archive_con_score(anger_dal_active)
update_db_con_score(dict_dal_active,"anger","dal_activ","anger_global_dict_count")

anger_dal_imag = get_lexical_archive("ConScore", "Dal_imag.csv")
dict_dal_imag = get_lexical_archive_con_score(anger_dal_imag)
update_db_con_score(dict_dal_imag,"anger","dal_imag","anger_global_dict_count")

anger_dal_pleas = get_lexical_archive("ConScore", "Dal_Pleas.csv")
dict_dal_pleas = get_lexical_archive_con_score(anger_dal_pleas)
update_db_con_score(dict_dal_pleas,"anger","dal_pleas","anger_global_dict_count")

