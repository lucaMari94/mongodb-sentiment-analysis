import mysql.connector
import re
import ast


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


def insert_db(dict_lexical_archive,db,emotion,type):

    for element in dict_lexical_archive:
        try:
            mycursor = db.cursor()
            sql = "INSERT INTO " + emotion + " (word, sentisense, type) VALUES (%s, %s, %s)"
            val = (element, 1, type)
            mycursor.execute(sql, val)
            db.commit()
        except mysql.connector.Error as e:
            print(e)


#############################################################################
# Hope


#Anticipation

db = connect_to_db()

dict_attribute_boolean = {"sentisense_hope.txt": 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Hope", element)
    print(dict_lexical_archive)
    insert_db(dict_lexical_archive,db,"anticipation","hope")


#############################################################################
# Trust

db = connect_to_db()

dict_attribute_boolean = {"sentisense_hope.txt": 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Hope", element)
    insert_db(dict_lexical_archive,db,"trust","hope")

    


#############################################################################
# Like

#Joy

db = connect_to_db()

dict_attribute_boolean = {"sentisense_like.txt": 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Like-Love", element)
    insert_db(dict_lexical_archive,db,"joy","like")
 


#Trust

db = connect_to_db()

dict_attribute_boolean = {"sentisense_like.txt": 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Like-Love", element)
    insert_db(dict_lexical_archive,db,"trust","like")


# Love

# Joy

db = connect_to_db()

dict_attribute_boolean = {"sentisense_love.txt": 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Like-Love", element)
    insert_db(dict_lexical_archive, db, "joy", "love")



#Trust

db = connect_to_db()

dict_attribute_boolean = {"sentisense_love.txt": 'sentisense'}

for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()
    dict_lexical_archive = get_lexical_archive("Like-Love", element)
    insert_db(dict_lexical_archive,db,"trust","love")


