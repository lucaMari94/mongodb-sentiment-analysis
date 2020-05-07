import re
import pymongo
import nltk
from bson import Code
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.corpus import wordnet as wn
from config import slang_words, posemoticons, negemoticons, other_emoticons, \
    EmojiPos, EmojiNeg, OthersEmoji, AdditionalEmoji, MyEmoji, punctuation


myfile = open("../twitter_message/dataset_dt_" + "anger" + "_60k.txt", "rt", encoding='utf-8')
contents = myfile.read()
myfile.close()

h_dictionary = []
emoticons_dictionary = []
emoji_dictionary = []


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
def process_emoji_and_emoticons(line, emoticons_dictionary, emoji_dictionary):

    # save to emoticons_dictionary and emoji_dictionary
    for word in line.split():
        if word in posemoticons:
            emoticons_dictionary.append(word)
        if word in negemoticons:
            emoticons_dictionary.append(word)
        if word in other_emoticons:
            emoticons_dictionary.append(word)
        if word in EmojiPos:
            emoji_dictionary.append(word)
        if word in EmojiNeg:
            emoji_dictionary.append(word)
        if word in OthersEmoji:
            emoji_dictionary.append(word)
        if word in AdditionalEmoji:
            emoji_dictionary.append(word)
        if word in MyEmoji:
            emoji_dictionary.append(word)

    # clear line
    for element in posemoticons:
        # emoticons_dictionary.append(element)
        line = line.replace(element, '')

    for element in negemoticons:
        # emoticons_dictionary.append(element)
        line = line.replace(element, '')

    for element in other_emoticons:
        # emoticons_dictionary.append(element)
        line = line.replace(element, '')

    for element in EmojiPos:
        # emoji_dictionary.append(element)
        line = line.replace(element, '')

    for element in EmojiNeg:
        # emoji_dictionary.append(element)
        line = line.replace(element, '')

    for element in OthersEmoji:
        # emoji_dictionary.append(element)
        line = line.replace(element, '')

    for element in AdditionalEmoji:
        # emoji_dictionary.append(element)
        line = line.replace(element, '')

    for element in MyEmoji:
        # emoji_dictionary.append(element)
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

"""
words = []
for line in contents.splitlines():
    # 1. remove URL and USERNAME
    line = remove_url_and_username(line)

    # 2. process hash-tag: collect hash-tag(#) (list)
    line = process_h(line, h_dictionary)

    # 3. process emoji and emoticons (list)
    line = process_emoji_and_emoticons(line, emoticons_dictionary, emoji_dictionary)

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

    # 10.5. optimization
    # remove words lenght == 1
    filtered_sentence_opt = [word for word in filtered_sentence if len(word) > 1]
    # remove number words
    filtered_sentence_opt = [word for word in filtered_sentence_opt if
                             not (word.isdigit() or word[0] == '-' and word[1:].isdigit())]

    # print(filtered_sentence_opt)
    # remove common words: i'm, get, go
    filtered_sentence_opt = [word for word in filtered_sentence_opt if word != "i'm"]
    filtered_sentence_opt = [word for word in filtered_sentence_opt if word != "get"]
    filtered_sentence_opt = [word for word in filtered_sentence_opt if word != "go"]

    # append array
    words.extend(filtered_sentence)
"""
client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

anger = db['anger']

# Remove any existing data: delete_many
# anger.remove()

# Insert the data: insert_one
# anger.insert({'word': word} for word in words)

anger_emoji = db['anger_emoji']
"""anger_emoji.remove()
anger_emoji.insert({'word': emoji} for emoji in emoji_dictionary)
"""

anger_emoticons = db['anger_emoticons']
"""anger_emoticons.remove()
anger_emoticons.insert({'word': emoticon} for emoticon in emoticons_dictionary)
"""

anger_hashtag = db['anger_hashtag']
"""anger_hashtag.remove()
anger_hashtag.insert({'word': hashtag} for hashtag in h_dictionary)
"""



# Load map and reduce functions
map = Code(open('wordMap.js', 'r').read())
reduce = Code(open('wordReduce.js', 'r').read())
"""
results = anger.map_reduce(map, reduce, "anger_frequency")"""

anger_emoticons.map_reduce(map, reduce, "anger_emoticons_frequency")

"""anger_emoji.map_reduce(map, reduce, "anger_emoji_frequency")
anger_emoticons.map_reduce(map, reduce, "anger_emoticons_frequency")"""
# anger_hashtag.map_reduce(map, reduce, "anger_hashtag_frequency")
"""
anger_hashtag_frequency = db['anger_hashtag_frequency']
for x in anger_hashtag_frequency.find():
  print(x)"""
# Print the results
"""for result in results.find():
    print(result['_id'], result['value']['count'])"""

anger_emoticons_frequency = db['anger_emoticons_frequency']

total = 0
for result in anger_emoticons_frequency.find():
    total += result['value']['count']
    # print(result['_id'], result['value']['count'])
print(total)