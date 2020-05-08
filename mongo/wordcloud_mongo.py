import string
from PIL import Image
import numpy as np
import pymongo
from wordcloud import WordCloud, STOPWORDS
from os import path
import os

client = pymongo.MongoClient("mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass%20Community"
                             "&ssl=false&retryWrites=false&w=majority")

db = client['emotion']

dataset_sentiment = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

for emotion in dataset_sentiment:

    emotion_word = db[emotion + '_frequency']
    emotion_emoji = db[emotion + '_emoji_frequency']
    emotion_emoticons = db[emotion + '_emoticons_frequency']
    emotion_hashtag = db[emotion + '_hashtag_frequency']

    dict_emotion_frequency = {}
    dict_emotion_frequency.clear()

    dict_emotion_emoji = {}
    dict_emotion_emoji.clear()

    dict_emotion_emoticons = {}
    dict_emotion_emoticons.clear()

    dict_emotion_hashtag = {}
    dict_emotion_hashtag.clear()

    # words
    for element in emotion_word.find():
        dict_emotion_frequency[element["_id"]] = element["value"]["count"]

    # emoji
    for element in emotion_emoji.find():
        dict_emotion_emoji[element["_id"]] = element["value"]["count"]

    # emoticons
    for element in emotion_emoticons.find():
        dict_emotion_emoticons[element["_id"]] = element["value"]["count"]

    # hashtag
    for element in emotion_hashtag.find():
        dict_emotion_hashtag[element["_id"]] = element["value"]["count"]

    twitter_mask = np.array(Image.open("../img/twitter.jpg"))

    wc = WordCloud(width=512, height=512, background_color='white', stopwords=STOPWORDS,
                   mask=twitter_mask)
    # words
    wc.generate_from_frequencies(dict_emotion_frequency)
    wc.to_file("../img_mongo/" + emotion + "_dict_wordcloud.jpg")

    # hastag
    wc.generate_from_frequencies(dict_emotion_hashtag)
    wc.to_file("../img_mongo/" + emotion + "_hashtag_wordcloud.jpg")

    # emoticons
    normal_word = r"(?:\w[\w'-]+)"
    ascii_art = r"(?:[{punctuation}][{punctuation}]+)".format(punctuation=string.punctuation)
    regexp = r"{normal_word}|{ascii_art}".format(normal_word=normal_word, ascii_art=ascii_art)

    wc_emoticons = WordCloud(width=512, height=512, background_color='white', regexp=regexp, mask=twitter_mask)

    wc_emoticons.generate_from_frequencies(dict_emotion_emoticons)
    wc_emoticons.to_file("../img_mongo/" + emotion + "_emoticons_wordcloud.jpg")

    # emoji
    emoji_format = r"(?:[^\s])(?<![\w{ascii_printable}])".format(ascii_printable=string.printable)
    regexp = r"{emoji}".format(emoji=emoji_format)

    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    font_path = path.join(d, '../fonts', 'Symbola', 'Symbola.ttf')

    wc_emoji = WordCloud(width=512, height=512, background_color='white', mask=twitter_mask,
                         regexp=regexp, font_path=font_path)

    wc_emoji.generate_from_frequencies(dict_emotion_emoji)
    wc_emoji.to_file("../img_mongo/" + emotion + "_emoji_wordcloud.jpg")