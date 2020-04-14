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
    myfile = open("archive_risorse_lessicali/"+ foldername + "/" + filename + ".txt", "rt", encoding='utf-8')
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

def update_db(words, table_name, attributename, result_count_dict):
    # read file dictionary
    myfile = open("result_count/"+ result_count_dict +".txt", "rt", encoding='utf-8')
    contents_twit = myfile.read()
    myfile.close()
    dict_twit = ast.literal_eval(contents_twit)

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

# anger
# emosn, nrc, sentisense
anger_emosn = get_lexical_archive("Anger", "EmoSN_anger")
update_db(anger_emosn, 'anger', 'emo_sn', 'anger_global_dict_count')

anger_nrc = get_lexical_archive("Anger", "NRC_anger")
update_db(anger_nrc, 'anger', 'nrc', 'anger_global_dict_count')

anger_sentisense = get_lexical_archive("Anger", "sentisense_anger")
update_db(anger_sentisense, 'anger', 'sentisense', 'anger_global_dict_count')