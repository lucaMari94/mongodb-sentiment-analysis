import json

from pymongo import MongoClient
from bson.code import Code
from config import slang_words, posemoticons, negemoticons, other_emoticons, \
    EmojiPos, EmojiNeg, OthersEmoji, AdditionalEmoji, MyEmoji, punctuation
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk import FreqDist
import re

# http://aimotion.blogspot.com/2010/08/mapreduce-with-mongodb-and-python.html

# 1. remove URL and USERNAME (anonymization)
def remove_url_and_username(line):
    line = line.replace('URL', '')
    line = line.replace('USERNAME', '')
    return line


# 2. process hash-tag: collect hash-tag(#) (list)
def process_h(line, h_dictionary):
    # hashtag array [string, ...]
    h_array = re.findall(r"#(\w+)", line)

    for element in h_array:
        h_dictionary.append(element)
        line = line.replace('#'+element, '')
    return line


# 3. process emoji and emoticons (list)
def process_emoji_and_emoticons(line):
    for element in posemoticons:
        line = line.replace(element, '')

    for element in negemoticons:
        line = line.replace(element, '')

    for element in other_emoticons:
        line = line.replace(element, '')

    for element in EmojiPos:
        line = line.replace(element, '')

    for element in EmojiNeg:
        line = line.replace(element, '')

    for element in OthersEmoji:
        line = line.replace(element, '')

    for element in AdditionalEmoji:
        line = line.replace(element, '')

    for element in MyEmoji:
        line = line.replace(element, '')

    return line


# 4. treatment punctuation marks and substitution with spaces
def treatment_punctuation(line):
    for element in punctuation:
        line = line.replace(element, '')

    return line


# 7. process slang word and acronyms (list)
def replace_slang(tokens):
    for i, element in enumerate(tokens):
        for slang_word in slang_words:
            if element == slang_word:
                tokens[i] = slang_words.get(slang_word)
    return tokens


"""
    Convert POS tag from Penn tagset to WordNet tagset.
    :param tag: a tag from Penn tagset
    :return: a tag from WordNet tagset or None if no corresponding tag could be found
"""
def pos_tag_convert(tag):
    """if tag in ['JJ', 'JJR', 'JJS']:
        return wn.ADJ
    elif tag in ['RB', 'RBR', 'RBS']:
        return wn.ADV
    elif tag in ['NN', 'NNS', 'NNP', 'NNPS']:
        return wn.NOUN
    elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return wn.VERB
    return None"""
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('V'):
        return wn.VERB
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    else:
        return None


def lemmatization(lemmatizer, tagged):
    result_lemma = []
    for element, tag in tagged:
        pos_tag = pos_tag_convert(tag)
        if pos_tag is None:
            result_lemma.append(element)
        else:
            # print(pos_tag_convert(tag))
            lemma = lemmatizer.lemmatize(element, pos_tag)
            result_lemma.append(lemma)
    return result_lemma


def processing(h_dictionary, words):

    # myfile = open("words.txt", "rt", encoding='utf-8')
    myfile = open("../twitter_message/dataset_dt_" + "anger" + "_60k.txt", "rt", encoding='utf-8')
    lines = myfile.read()
    myfile.close()

    for line in lines.splitlines():

        # 1. remove URL and USERNAME
        line = remove_url_and_username(line)

        # 2. process hash-tag: collect hash-tag(#) (list)
        line = process_h(line, h_dictionary)

        # 3. process emoji and emoticons (list)
        line = process_emoji_and_emoticons(line)

        # 4. treatment punctuation marks and substitution with spaces
        line = treatment_punctuation(line)

        # 5. transformation to lower case
        line = line.lower()

        # 6. sentence tokenisation
        # tokens = nltk.word_tokenize(line)
        tknzr = TweetTokenizer()
        tokens = tknzr.tokenize(line)

        # 7. process slang word and acronyms (list)
        tokens = replace_slang(tokens)

        # 8. POS tagging
        tagged = nltk.pos_tag(tokens)
        # print(tagged)

        # 9. lemmatization
        lemmatizer = WordNetLemmatizer()
        result_lemma = lemmatization(lemmatizer, tagged)

        # 10. stop words elimination
        stop_words = set(stopwords.words('english'))
        filtered_sentence = [word for word in result_lemma if not word in stop_words]
        # print(filtered_sentence)
        words.extend(filtered_sentence)
        # return filtered_sentence

# client
connection = MongoClient('localhost', 27021)
db = connection.test

# insert data
h_dictionary = []

# global dictionary count
words = []
processing(h_dictionary, words)

words_dictionary = []
for word in words:
    x = {
        "word": word
    }
    words_dictionary.append(x)

# print(words)
file = open("result.json", "w", encoding='utf-8')
file.write(json.dumps(words_dictionary))
file.close()
# myfile = open("words.txt", "rt", encoding='utf-8')
# [db.anger.insert_one({'word': word}) for word in words]

"""
# load map and reduce functions
map = Code(open('wordMap.js', 'r').read())
reduce = Code(open('wordReduce.js', 'r').read())

# run the map-reduce query
results = db.texts.map_reduce(map, reduce, "output")

for result in results.find():
    print(result['_id'], result['value']['count'])"""
