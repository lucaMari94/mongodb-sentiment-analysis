import nltk
from nltk.tokenize import TweetTokenizer
from config import slang_words
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import FreqDist


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


# 7. process slang word and acronyms (list)
def replace_slang(tokens):
    for i, element in enumerate(tokens):
        for slang_word in slang_words:
            if element == slang_word:
                tokens[i] = slang_words.get(slang_word)
    return tokens

text = "pretty legit @ atm the disney galleries"

tknzr = TweetTokenizer()
tokens = tknzr.tokenize(text)
print(tokens)
# 7. process slang word and acronyms (list)
tokens = replace_slang(tokens)
print(tokens)
# 8. POS tagging
tagged = nltk.pos_tag(tokens)
print(tagged)

# 9. lemmatization
lemmatizer = WordNetLemmatizer()
result_lemma = lemmatization(lemmatizer, tagged)
print(result_lemma)

# 10. stop words elimination
stop_words = set(stopwords.words('english'))
filtered_sentence = [word for word in result_lemma if not word in stop_words]
print(filtered_sentence)

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

# 11. stem frequency counting (for each word)
frequency_dist = FreqDist(filtered_sentence_opt)
frequency_array = frequency_dist.most_common()
print(frequency_dist)
print(frequency_array)