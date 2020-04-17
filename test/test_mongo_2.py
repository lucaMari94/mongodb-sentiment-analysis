import ast
from pymongo import MongoClient

############################
# to do sharding
# node1: part1 of tweet message
# node2: part2 of tweet message
# node3: part3 of tweet message
# -----------------------------
# for node1, node2, node3
# map(sentiment,MI)
# che processa i Tweets nell’insieme di Tweets in MI associati al sentimento
# sentiment e costruisce una mappa che ha la forma della mappa annidata
# vista nella slide precedente; ogni Tweet in MI verrà processato secondo
# le stesse linee guida (pipeline sequenziale di elaborazione dei Tweets)
# viste già per il Laboratorio con Oracle e verificherà la presenza delle
# parole nella mappa (se non presenti, le aggiungerà alla mappa) come
# chiave e come valore avrà il numero dei Tweets in MI con quella parola.
# -----------------------------
# Reduce(sentiment,MI)
# che prenderà dai vari nodi I le mappe MI e farà il merge delle
# mappe che avranno lo stesso valore di sentiment. Il merge farà la
# somma delle frequenze delle stesse chiavi (parole) nelle varie
# mappe. produrrà una mappa M globale per ogni sentimento
# -----------------------------
# Filter(K)
# che filtrerà le mappe M con le K chiavi che hanno il valore
# maggiore. Produrrà una mappa MK per ogni sentimento.
# Le mappe MK saranno l’input al software di Word Cloud
# (che produrrà una nuvola di parole di dimensione variabile a seconda della frequenza)
############################

# read from file
# read file
myfile = open("../twitter_message/dataset_dt_" + "anger" + "_60k.txt", "rt", encoding='utf-8')
contents = myfile.read()
myfile.close()

"""
def map(document, word):
    if word in document:
        return 1
    else:
        return 0


def reduce(list_values_mapped):
    cont = 0
    for i in list_values_mapped:
        if i == 1:
            cont += 1
    return cont
"""


def multiply2(x):
    return x * 2


# Output [2, 4, 6, 8]
print(list(map(multiply2, [1, 2, 3, 4])))


dict_a = [{'name': 'python', 'points': 10}, {'name': 'java', 'points': 8}]
map(lambda x: x['name'], dict_a)  # Output: ['python', 'java']
map(lambda x: x['points'] * 10, dict_a)  # Output: [100, 80]
map(lambda x: x['name'] == "python", dict_a)  # Output: [True, False]


list_a = [1, 2, 3]
list_b = [10, 20, 30]
map(lambda x, y: x + y, list_a, list_b)  # Output: [11, 22, 33]


map_output = map(lambda x: x*2, [1, 2, 3, 4])
print(map_output) # Output: map object: <map object at 0x04D6BAB0>
list_map_output = list(map_output)
print(list_map_output) # Output: [2, 4, 6, 8]


#filter


a = [1, 2, 3, 4, 5, 6]
filter(lambda x : x % 2 == 0, a) # Output: [2, 4, 6]


dict_a = [{'name': 'python', 'points': 10}, {'name': 'java', 'points': 8}]
filter(lambda x : x['name'] == 'python', dict_a) # Output: [{'name': 'python', 'points': 10}]


list_a = [1, 2, 3, 4, 5]
filter_obj = filter(lambda x: x % 2 == 0, list_a) # filter object <filter at 0x4e45890>
even_num = list(filter_obj) # Converts the filer obj to a list
print(even_num) # Output: [2, 4]

"""db.words.insert = {[
 {lemma:“nice”,
 lexical_resources:{
 EmoSN: 1, SentiSense: 1, NRC: 1, GI_POS: 1,
 ANEW:{score:1.3},
 DAL:{arousal: 1.3, dominance: 0.7, pleaseness: 0.5}
 },
 frequency=127},
 {lemma=“afraid”,lexical_resources={…}, frequency=..},
]}"""

"""
# client
client = MongoClient('localhost', 27017)

# access to db
db = client.words

# access to table/collection
collection = db.words
data = { "lemma":"nice", "lexical_resources": { "EmoSN": 1, "SentiSense": 1, "NRC": 1, "GI_POS": 1,
                              "ANEW" : {"score":1.3},
                              "DAL":{ "arousal": 1.3, "dominance": 0.7, "pleaseness": 0.5}
                            },
  "frequency" : 127},
collection.insert_many(data)"""
