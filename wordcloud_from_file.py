import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import ast
import matplotlib.pyplot as plt

# read from file
def load_emotion_from_dict(emotion):
    myfile = open("result_count/global_dict_count_" + emotion, "rt", encoding='utf-8')
    dict = myfile.read()
    myfile.close()
    return dict

def load_emotion_from_hashtag(emotion):
    myfile = open("result_count/hashtag_" + emotion, "rt", encoding='utf-8')
    dict = myfile.read()
    myfile.close()
    return dict

def create_wordcloud(emotion, flag):

    # read from file
    if flag:
        # Generate a wordcloud from dict
        string_dict = load_emotion_from_dict(emotion)
        # trasform string to dictionary
        dict = ast.literal_eval(string_dict)

    else:
        string_dict = load_emotion_from_dict(emotion)

    # wordcloud
    twitter_mask = np.array(Image.open("img/twitter.jpg"))

    # Create a word cloud image
    wc = WordCloud(stopwords=STOPWORDS, background_color="white", max_words=500, mask=twitter_mask, contour_width=1)

    if flag:
        # Generate a wordcloud from dict
        wc.generate_from_frequencies(dict)
        wc.to_file("img/twitter_" + emotion + ".jpg")
    else:
        wc.generate(string_dict)
        wc.to_file("img/twitter_hashtag_" + emotion + ".jpg")

    # store to file

    # show
    # plt.figure(figsize=[20, 10])
    # plt.imshow(wc)
    # plt.axis("off")
    # plt.show()

dataset_sentiment = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

for emotion in dataset_sentiment:
    create_wordcloud(emotion, True)

for emotion in dataset_sentiment:
    create_wordcloud(emotion, False)