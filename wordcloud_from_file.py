import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import ast
import matplotlib.pyplot as plt

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

dataset_sentiment = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

# dictionary
for emotion in dataset_sentiment:

     string_dict = load_emotion_from_dict(emotion)
     dict = ast.literal_eval(string_dict)

     twitter_mask = np.array(Image.open("img/twitter.jpg"))

     wc = WordCloud(width=512, height=512, background_color='white', stopwords=STOPWORDS, mask=twitter_mask)
     wc.generate_from_frequencies(dict)

     wc.to_file("img/" + emotion + "_dict_wordcloud.jpg")

     """plt.figure(figsize=(10, 8), facecolor='white', edgecolor='blue')
    plt.imshow(wc)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()"""

# hashtag
for emotion in dataset_sentiment:
    hashtag = load_emotion_from_hashtag(emotion)

    twitter_mask = np.array(Image.open("img/twitter.jpg"))

    wc = WordCloud(width=512, height=512, background_color='white', stopwords=STOPWORDS, mask=twitter_mask)
    wc.generate(hashtag)

    wc.to_file("img/" + emotion + "_hashtag_wordcloud.jpg")

    """plt.figure(figsize=(10, 8), facecolor='white', edgecolor='blue')
    plt.imshow(wc)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()"""
