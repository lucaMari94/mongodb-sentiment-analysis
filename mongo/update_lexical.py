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


def get_lexical_archive_con_score(dict):
    dict_con_score = {}

    for element in dict:
        array = element.split("\t")
        dict_con_score[array[0]] = array[1]

    return dict_con_score


def update_record(foldername_lexical_archive, file_lexical_archive, field, emotion_frequency_collection):

    lexical_archive = []
    lexical_archive = get_lexical_archive(foldername_lexical_archive, file_lexical_archive)
    # print(lexical_archive)
    for word in lexical_archive:

        mongo_record = emotion_frequency_collection.find_one({"_id": word})

        if mongo_record != None:
            # print(mongo_record)
            result = emotion_frequency_collection.update_one(
                {"_id": word},
                {"$addToSet": {"lexical_resources": {field: 1}}}
            )
            # init_values["$set"]["lexical_resources"][field] = 1
            # anger_frequency_collection.update_one(mongo_record, init_values)


def update_record_con_score(dict_lexical_archive, field, emotion_frequency_collection):

    for word in dict_lexical_archive:
        mongo_record = emotion_frequency_collection.find_one({"_id": word})

        if mongo_record != None:
            # print(mongo_record)
            result = emotion_frequency_collection.update_one(
                {"_id": word},
                {"$addToSet": {"lexical_resources": {field: dict_lexical_archive.get(word)}}}
            )
            # init_values["$set"]["lexical_resources"][field] = 1
            # anger_frequency_collection.update_one(mongo_record, init_values)


client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

# anger
anger_frequency_collection = db["anger_frequency"]
anger_frequency_collection.update_many({}, {"$set": {"lexical_resources": []}})

# for boolean attribute : set 1 if present in dictionary twitter
update_record("Anger", "EmoSN_anger.txt", "EmoSN", anger_frequency_collection)
update_record("Anger", "NRC_anger.txt", "NRC", anger_frequency_collection)
update_record("Anger", "sentisense_anger.txt", "SentiSense", anger_frequency_collection)

# Neg
update_record("Neg", "GI_NEG.txt", "GI_NEG", anger_frequency_collection)
update_record("Neg", "HL-negatives.txt", "HL_NEG", anger_frequency_collection)
update_record("Neg", "listNegEffTerms.txt", "LIST_NEG", anger_frequency_collection)
update_record("Neg", "LIWC-NEG.txt", "LIWC_NEG", anger_frequency_collection)

# Pos
update_record("Pos", "GI_POS.txt", "GI_POS", anger_frequency_collection)
update_record("Pos", "HL-positives.txt", "HL_POS", anger_frequency_collection)
update_record("Pos", "listPosEffTerms.txt", "LIST_POS", anger_frequency_collection)
update_record("Pos", "LIWC-POS.txt", "LIWC_POS", anger_frequency_collection)

# Con Score
dict = get_lexical_archive("ConScore", "afinn.txt")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "AFINN", anger_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewAro_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_ARO", anger_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewDom_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_DOM", anger_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewPleas_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_PLEAS", anger_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Activ.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_ACTIV", anger_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Imag.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_IMAG", anger_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Pleas.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_PLEAS", anger_frequency_collection)

#################################################################

# anticipation
anticipation_frequency_collection = db["anticipation_frequency"]
anticipation_frequency_collection.update_many({}, {"$set": {"lexical_resources": []}})

# for boolean attribute : set 1 if present in dictionary twitter
update_record("Anticipation", "NRC_anticipation.txt", "NRC", anticipation_frequency_collection)
update_record("Anticipation", "sentisense_anticipation.txt", "SentiSense", anticipation_frequency_collection)

# Neg
update_record("Neg", "GI_NEG.txt", "GI_NEG", anticipation_frequency_collection)
update_record("Neg", "HL-negatives.txt", "HL_NEG", anticipation_frequency_collection)
update_record("Neg", "listNegEffTerms.txt", "LIST_NEG", anticipation_frequency_collection)
update_record("Neg", "LIWC-NEG.txt", "LIWC_NEG", anticipation_frequency_collection)

# Pos
update_record("Pos", "GI_POS.txt", "GI_POS", anticipation_frequency_collection)
update_record("Pos", "HL-positives.txt", "HL_POS", anticipation_frequency_collection)
update_record("Pos", "listPosEffTerms.txt", "LIST_POS", anticipation_frequency_collection)
update_record("Pos", "LIWC-POS.txt", "LIWC_POS", anticipation_frequency_collection)

# Con Score
dict = get_lexical_archive("ConScore", "afinn.txt")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "AFINN", anticipation_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewAro_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_ARO", anticipation_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewDom_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_DOM", anticipation_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewPleas_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_PLEAS", anticipation_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Activ.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_ACTIV", anticipation_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Imag.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_IMAG", anticipation_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Pleas.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_PLEAS", anticipation_frequency_collection)

#################################################################

# disgust

disgust_frequency_collection = db["disgust_frequency"]
disgust_frequency_collection.update_many({}, {"$set": {"lexical_resources": []}})

# for boolean attribute : set 1 if present in dictionary twitter
update_record("Disgust-Hate", "NRC_disgust.txt", "NRC", disgust_frequency_collection)
update_record("Disgust-Hate", "sentisense_disgust.txt", "SentiSense", disgust_frequency_collection)
update_record("Disgust-Hate", "sentisense_hate.txt", "SentiSense", disgust_frequency_collection)

# Neg
update_record("Neg", "GI_NEG.txt", "GI_NEG", disgust_frequency_collection)
update_record("Neg", "HL-negatives.txt", "HL_NEG", disgust_frequency_collection)
update_record("Neg", "listNegEffTerms.txt", "LIST_NEG", disgust_frequency_collection)
update_record("Neg", "LIWC-NEG.txt", "LIWC_NEG", disgust_frequency_collection)

# Pos
update_record("Pos", "GI_POS.txt", "GI_POS", disgust_frequency_collection)
update_record("Pos", "HL-positives.txt", "HL_POS", disgust_frequency_collection)
update_record("Pos", "listPosEffTerms.txt", "LIST_POS", disgust_frequency_collection)
update_record("Pos", "LIWC-POS.txt", "LIWC_POS", disgust_frequency_collection)

# Con Score
dict = get_lexical_archive("ConScore", "afinn.txt")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "AFINN", disgust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewAro_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_ARO", disgust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewDom_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_DOM", disgust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewPleas_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_PLEAS", disgust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Activ.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_ACTIV", disgust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Imag.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_IMAG", disgust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Pleas.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_PLEAS", disgust_frequency_collection)



#################################################################

# fear

fear_frequency_collection = db["fear_frequency"]
fear_frequency_collection.update_many({}, {"$set": {"lexical_resources": []}})

# for boolean attribute : set 1 if present in dictionary twitter
update_record("Fear", "NRC_fear.txt", "NRC", fear_frequency_collection)
update_record("Fear", "sentisense_fear.txt", "SentiSense", fear_frequency_collection)

# Neg
update_record("Neg", "GI_NEG.txt", "GI_NEG", fear_frequency_collection)
update_record("Neg", "HL-negatives.txt", "HL_NEG", fear_frequency_collection)
update_record("Neg", "listNegEffTerms.txt", "LIST_NEG", fear_frequency_collection)
update_record("Neg", "LIWC-NEG.txt", "LIWC_NEG", fear_frequency_collection)

# Pos
update_record("Pos", "GI_POS.txt", "GI_POS", fear_frequency_collection)
update_record("Pos", "HL-positives.txt", "HL_POS", fear_frequency_collection)
update_record("Pos", "listPosEffTerms.txt", "LIST_POS", fear_frequency_collection)
update_record("Pos", "LIWC-POS.txt", "LIWC_POS", fear_frequency_collection)

# Con Score
dict = get_lexical_archive("ConScore", "afinn.txt")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "AFINN", fear_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewAro_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_ARO", fear_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewDom_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_DOM", fear_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewPleas_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_PLEAS", fear_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Activ.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_ACTIV", fear_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Imag.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_IMAG", fear_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Pleas.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_PLEAS", fear_frequency_collection)

#################################################################

# hope

hope_frequency_collection = db["hope_frequency"]
hope_frequency_collection.update_many({}, {"$set": {"lexical_resources": []}})

# for boolean attribute : set 1 if present in dictionary twitter
update_record("Hope", "sentisense_hope.txt", "NRC", hope_frequency_collection)

# Neg
update_record("Neg", "GI_NEG.txt", "GI_NEG", hope_frequency_collection)
update_record("Neg", "HL-negatives.txt", "HL_NEG", hope_frequency_collection)
update_record("Neg", "listNegEffTerms.txt", "LIST_NEG", hope_frequency_collection)
update_record("Neg", "LIWC-NEG.txt", "LIWC_NEG", hope_frequency_collection)

# Pos
update_record("Pos", "GI_POS.txt", "GI_POS", hope_frequency_collection)
update_record("Pos", "HL-positives.txt", "HL_POS", hope_frequency_collection)
update_record("Pos", "listPosEffTerms.txt", "LIST_POS", hope_frequency_collection)
update_record("Pos", "LIWC-POS.txt", "LIWC_POS", hope_frequency_collection)

# Con Score
dict = get_lexical_archive("ConScore", "afinn.txt")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "AFINN", hope_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewAro_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_ARO", hope_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewDom_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_DOM", hope_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewPleas_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_PLEAS", hope_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Activ.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_ACTIV", hope_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Imag.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_IMAG", hope_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Pleas.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_PLEAS", hope_frequency_collection)

#################################################################

# joy

joy_frequency_collection = db["joy_frequency"]
joy_frequency_collection.update_many({}, {"$set": {"lexical_resources": []}})

# for boolean attribute : set 1 if present in dictionary twitter
update_record("Joy", "EmoSN_joy.txt", "EmoSN", joy_frequency_collection)
update_record("Joy", "NRC_joy.txt", "NRC", joy_frequency_collection)
update_record("Joy", "sentisense_joy.txt", "SentiSense", joy_frequency_collection)

# Neg
update_record("Neg", "GI_NEG.txt", "GI_NEG", joy_frequency_collection)
update_record("Neg", "HL-negatives.txt", "HL_NEG", joy_frequency_collection)
update_record("Neg", "listNegEffTerms.txt", "LIST_NEG", joy_frequency_collection)
update_record("Neg", "LIWC-NEG.txt", "LIWC_NEG", joy_frequency_collection)

# Pos
update_record("Pos", "GI_POS.txt", "GI_POS", joy_frequency_collection)
update_record("Pos", "HL-positives.txt", "HL_POS", joy_frequency_collection)
update_record("Pos", "listPosEffTerms.txt", "LIST_POS", joy_frequency_collection)
update_record("Pos", "LIWC-POS.txt", "LIWC_POS", joy_frequency_collection)

# Con Score
dict = get_lexical_archive("ConScore", "afinn.txt")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "AFINN", joy_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewAro_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_ARO", joy_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewDom_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_DOM", joy_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewPleas_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_PLEAS", joy_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Activ.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_ACTIV", joy_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Imag.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_IMAG", joy_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Pleas.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_PLEAS", joy_frequency_collection)

#################################################################

# sadness

sadness_frequency_collection = db["sadness_frequency"]
sadness_frequency_collection.update_many({}, {"$set": {"lexical_resources": []}})

# for boolean attribute : set 1 if present in dictionary twitter
update_record("Sadness", "NRC_sadness.txt", "NRC", sadness_frequency_collection)
update_record("Sadness", "sentisense_sadness.txt", "SentiSense", sadness_frequency_collection)

# Neg
update_record("Neg", "GI_NEG.txt", "GI_NEG", sadness_frequency_collection)
update_record("Neg", "HL-negatives.txt", "HL_NEG", sadness_frequency_collection)
update_record("Neg", "listNegEffTerms.txt", "LIST_NEG", sadness_frequency_collection)
update_record("Neg", "LIWC-NEG.txt", "LIWC_NEG", sadness_frequency_collection)

# Pos
update_record("Pos", "GI_POS.txt", "GI_POS", sadness_frequency_collection)
update_record("Pos", "HL-positives.txt", "HL_POS", sadness_frequency_collection)
update_record("Pos", "listPosEffTerms.txt", "LIST_POS", sadness_frequency_collection)
update_record("Pos", "LIWC-POS.txt", "LIWC_POS", sadness_frequency_collection)

# Con Score
dict = get_lexical_archive("ConScore", "afinn.txt")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "AFINN", sadness_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewAro_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_ARO", sadness_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewDom_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_DOM", sadness_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewPleas_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_PLEAS", sadness_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Activ.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_ACTIV", sadness_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Imag.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_IMAG", sadness_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Pleas.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_PLEAS", sadness_frequency_collection)

#################################################################

# surprise

surprise_frequency_collection = db["surprise_frequency"]
surprise_frequency_collection.update_many({}, {"$set": {"lexical_resources": []}})

# for boolean attribute : set 1 if present in dictionary twitter
update_record("Surprise", "NRC_surprise.txt", "NRC", surprise_frequency_collection)
update_record("Surprise", "sentisense_surprise.txt", "SentiSense", surprise_frequency_collection)

# Neg
update_record("Neg", "GI_NEG.txt", "GI_NEG", surprise_frequency_collection)
update_record("Neg", "HL-negatives.txt", "HL_NEG", surprise_frequency_collection)
update_record("Neg", "listNegEffTerms.txt", "LIST_NEG", surprise_frequency_collection)
update_record("Neg", "LIWC-NEG.txt", "LIWC_NEG", surprise_frequency_collection)

# Pos
update_record("Pos", "GI_POS.txt", "GI_POS", surprise_frequency_collection)
update_record("Pos", "HL-positives.txt", "HL_POS", surprise_frequency_collection)
update_record("Pos", "listPosEffTerms.txt", "LIST_POS", surprise_frequency_collection)
update_record("Pos", "LIWC-POS.txt", "LIWC_POS", surprise_frequency_collection)

# Con Score
dict = get_lexical_archive("ConScore", "afinn.txt")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "AFINN", surprise_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewAro_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_ARO", surprise_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewDom_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_DOM", surprise_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewPleas_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_PLEAS", surprise_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Activ.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_ACTIV", surprise_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Imag.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_IMAG", surprise_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Pleas.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_PLEAS", surprise_frequency_collection)

#################################################################

# trust

trust_frequency_collection = db["trust_frequency"]
trust_frequency_collection.update_many({}, {"$set": {"lexical_resources": []}})

# for boolean attribute : set 1 if present in dictionary twitter
update_record("Trust", "NRC_trust.txt", "NRC", trust_frequency_collection)

# Neg
update_record("Neg", "GI_NEG.txt", "GI_NEG", trust_frequency_collection)
update_record("Neg", "HL-negatives.txt", "HL_NEG", trust_frequency_collection)
update_record("Neg", "listNegEffTerms.txt", "LIST_NEG", trust_frequency_collection)
update_record("Neg", "LIWC-NEG.txt", "LIWC_NEG", trust_frequency_collection)

# Pos
update_record("Pos", "GI_POS.txt", "GI_POS", trust_frequency_collection)
update_record("Pos", "HL-positives.txt", "HL_POS", trust_frequency_collection)
update_record("Pos", "listPosEffTerms.txt", "LIST_POS", trust_frequency_collection)
update_record("Pos", "LIWC-POS.txt", "LIWC_POS", trust_frequency_collection)

# Con Score
dict = get_lexical_archive("ConScore", "afinn.txt")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "AFINN", trust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewAro_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_ARO", trust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewDom_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_DOM", trust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "anewPleas_tab.tsv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "ANEW_PLEAS", trust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Activ.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_ACTIV", trust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Imag.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_IMAG", trust_frequency_collection)

dict.clear()
dict_con_score.clear()
dict = get_lexical_archive("ConScore", "Dal_Pleas.csv")
dict_con_score = get_lexical_archive_con_score(dict)
update_record_con_score(dict_con_score, "DAL_PLEAS", trust_frequency_collection)