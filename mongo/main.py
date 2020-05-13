import re
import pymongo
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.corpus import wordnet as wn
from config import slang_words, posemoticons, negemoticons, other_emoticons, \
    EmojiPos, EmojiNeg, OthersEmoji, AdditionalEmoji, MyEmoji, punctuation


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


def processing(emotion, words, h_dictionary, emoticons_dictionary, emoji_dictionary):

    myfile = open("../twitter_message/dataset_dt_" + emotion + "_60k.txt", "rt", encoding='utf-8')
    contents = myfile.read()
    myfile.close()

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
        words.extend(filtered_sentence_opt)

    return {
        "words": words,
        "h_dictionary": h_dictionary,
        "emoticons_dictionary": emoticons_dictionary,
        "emoji_dictionary": emoji_dictionary
    }


client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

dataset_sentiment = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

for emotion in dataset_sentiment:

    # words array
    words = []

    # hashtag_dictionary array
    h_dictionary = []

    # emoticons_dictionary array
    emoticons_dictionary = []

    # emoji_dictionary array
    emoji_dictionary = []

    result = processing(emotion, words, h_dictionary, emoticons_dictionary, emoji_dictionary)

    words = result.get('words')

    with open('words.txt', 'w', encoding="utf-8") as f:
        for item in words:
            f.write("%s\n" % item)

    h_dictionary = result.get('h_dictionary')
    emoticons_dictionary = result.get('emoticons_dictionary')
    emoji_dictionary = result.get('emoji_dictionary')

    emotion_word = db[emotion + '_word']
    emotion_word.remove()
    emotion_word.insert({'word': word} for word in words)

    emotion_hashtag = db[emotion + '_hashtag']
    emotion_hashtag.remove()
    emotion_hashtag.insert({'word': hashtag} for hashtag in h_dictionary)

    emotion_emoticons = db[emotion + '_emoticons']
    emotion_emoticons.remove()
    emotion_emoticons.insert({'word': emoticon} for emoticon in emoticons_dictionary)

    emotion_emoji = db[emotion + '_emoji']
    emotion_emoji.remove()
    emotion_emoji.insert({'word': emoji} for emoji in emoji_dictionary)