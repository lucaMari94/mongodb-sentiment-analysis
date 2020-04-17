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

print(contents)

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
collection.insert_many(data)
