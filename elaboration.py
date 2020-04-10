import re
import time
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk import FreqDist
from config import slang_words, posemoticons, negemoticons, other_emoticons, \
    EmojiPos, EmojiNeg, OthersEmoji, AdditionalEmoji, MyEmoji, punctuation

# hashtag array
h_dictionary = []

# global dictionary count
global_dict_count = {}

# 1. remove URL and USERNAME (anonymization)
def remove_url_and_username(line):
    line = line.replace('URL', '')
    line = line.replace('USERNAME', '')
    return line

# 2. process hash-tag: collect hash-tag(#) (list)
def process_h(line):
    pat = re.compile(r"#(\w+)")

    # hashtag array [string, ...]
    h_array = pat.findall(line)
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

# (get, 10)
# 12. adding to dictionary
def adding_to_dictionary(frequency_array):
    for element in frequency_array:
        # element[0] = word
        # element[1] = count

        if element[0] in global_dict_count.keys():
            global_dict_count[element[0]] = global_dict_count.get(element[0]) + 1
        else:
            global_dict_count[element[0]] = element[1]

def processing(emotion):
    # read file
    myfile = open("twitter_message/dataset_dt_" + emotion + "_60k.txt", "rt", encoding='utf-8')
    contents = myfile.read()
    myfile.close()
    t0 = time.time()

    for line in contents.splitlines():
        # 1. remove URL and USERNAME
        line = remove_url_and_username(line)

        # 2. process hash-tag: collect hash-tag(#) (list)
        line = process_h(line)

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

        # 11. stem frequency counting (for each word)
        frequency_dist = FreqDist(filtered_sentence)
        frequency_array = frequency_dist.most_common()
        # print(frequency_array)

        # 12. adding to dictionary
        adding_to_dictionary(frequency_array)

    # timer
    t1 = time.time()
    total = t1 - t0

    file = open("result_count/global_dict_count_" + emotion, "a", encoding='utf-8')
    file.write(json.dumps(global_dict_count))
    file.close()
    print(total)

# filename dataset_sentiment
dataset_sentiment = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"];

for emotion in dataset_sentiment:
    processing(emotion)