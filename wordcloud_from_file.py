import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import ast
import matplotlib.pyplot as plt
import string
from os import path
import os
import emoji

# read from file
def load_emotion_from_dict(emotion):
    myfile = open("result_count/" + emotion + "_global_dict_count.txt", "rt", encoding='utf-8')
    dict = myfile.read()
    myfile.close()
    return dict


def load_emotion_from_hashtag(emotion):
    myfile = open("result_count/" + emotion + "_hashtag.txt", "rt", encoding='utf-8')
    dict = myfile.read()
    myfile.close()
    return dict

#emoticons
def load_emoticons_from_dict(emotion):
    myfile = open("result_count/" + emotion + "_emoticons.txt", "rt", encoding='utf-8')
    dict = myfile.read()
    myfile.close()
    return dict

#emoji
def load_emoji_from_dict(emotion):
    myfile = open("result_count/" + emotion + "_emoji.txt", "rt", encoding='utf-8')
    dict = myfile.read()
    myfile.close()
    return dict


#dataset_sentiment = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

dataset_sentiment = ["anger", "anticipation", "disgust", "fear"]

"""
# dictionary
for emotion in dataset_sentiment:

     string_dict = load_emotion_from_dict(emotion)
     dict = ast.literal_eval(string_dict)

     twitter_mask = np.array(Image.open("img/twitter.jpg"))

    # max_words=50
     wc = WordCloud(width=512, height=512, background_color='white', stopwords=STOPWORDS, mask=twitter_mask)
     wc.generate_from_frequencies(dict)

     wc.to_file("img/" + emotion + "_dict_wordcloud.jpg")

"""  
# hashtag
for emotion in dataset_sentiment:
    hashtag = load_emotion_from_hashtag(emotion)

    twitter_mask = np.array(Image.open("img/twitter.jpg"))

    wc = WordCloud(width=512, height=512, background_color='white', collocations=False, stopwords=STOPWORDS, mask=twitter_mask)
    wc.generate(hashtag)

    wc.to_file("img/" + emotion + "_hashtag_wordcloud.jpg")


# emoticons
for emotion in dataset_sentiment:
    emoticons = load_emoticons_from_dict(emotion)

    twitter_mask = np.array(Image.open("img/twitter.jpg"))

    normal_word = r"(\:\w+\:|\<[\/\\]?3|[\(\)\\\D|\*\$][\-\^]?[\:\;\=]|[\:\;\=B8][\-\^]?[3DOPp\@\$\*\\\)\(\/\|])(?=\s|[\!\.\?]|$)"
    regexp = r"{normal_word}".format(normal_word = normal_word)

    wc = WordCloud(width=512, height=512, background_color='white',regexp=regexp, collocations=False, mask=twitter_mask)
    wc.generate(emoticons)

    wc.to_file("img/" + emotion + "_emoticons_wordcloud.jpg")

# emoji
for emotion in dataset_sentiment:

    emoji = load_emoji_from_dict(emotion)

    twitter_mask = np.array(Image.open("img/twitter.jpg"))

    emoji_format = r"(?:[^\s])(?<![\w{ascii_printable}])".format(ascii_printable=string.printable)
    regexp = r"{emoji}".format(emoji=emoji_format)


    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    font_path = path.join(d,'fonts', 'Symbola', 'Symbola.ttf')

    wc = WordCloud(width=512, height=512, font_path=font_path,regexp=regexp,collocations=False,background_color='white', mask=twitter_mask)
    wc.generate(emoji)

    wc.to_file("img/" + emotion + "_emoji_wordcloud.jpg")

    plt.figure(figsize=(10, 8), facecolor='white', edgecolor='blue')
    plt.imshow(wc)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

