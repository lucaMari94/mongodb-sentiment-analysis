import pymongo
import re


def get_lexical_archive(foldername, filename):
    # read file archive
    myfile = open("../archive_risorse_lessicali/" + foldername + "/" + filename, "rt", encoding='utf-8')
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


client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

# ANGER
dict_attribute_boolean = {"EmoSN_anger.txt": 'emo_sn',"NRC_anger.txt": 'nrc'}

# "NRC_anger.txt": 'nrc',
# "sentisense_anger.txt": 'sentisense'}

mycol = db["anger_frequency"]

newvalues = {}
for element in dict_attribute_boolean:
    dict_lexical_archive = {}
    dict_lexical_archive.clear()

    # lexical_archive array(EMOSN,NRC,sentisence 3 row)
    dict_lexical_archive = get_lexical_archive("Anger", element)
    newvalues = {"$set": {"lexical_resources": {dict_attribute_boolean.get(element): 0}}}
print(newvalues)

"""
    for word in dict_lexical_archive:
        
        myquery = { "_id": word }

        mongo_record=mycol.find_one({"_id": word})
        print("---------------------------")

        if mongo_record !=None:
            print(mongo_record)
            print(dict_attribute_boolean.get(element))
            newvalues["$set"]["lexical_resources"][dict_attribute_boolean.get(element)] = 1
            print(newvalues)


            #mycol.update_one(mongo_record, newvalues)
            #print(dict_attribute_boolean.get(element))
           # print(mongo_record)

           # newvalues = { "$set": { dict_attribute_boolean.get(element): 1 } }

"""

"""
lexical_resources:{
EmoSN: 1, SentiSense: 1, NRC: 1, GI_POS: 1,
ANEW:{score:1.3},
DAL:{arousal: 1.3, dominance: 0.7, pleaseness: 0.5}
},

mycol.update_one(myquery, newvalues)

#print "customers" after the update:
for x in mycol.find():
  print(x)
"""
