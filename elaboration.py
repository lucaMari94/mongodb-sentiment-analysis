import re
from config import slang_words, posemoticons, negemoticons, other_emoticons, \
    EmojiPos, EmojiNeg, OthersEmoji, AdditionalEmoji, MyEmoji, punctuation

# hashtag array
h_dictionary = []

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

# filename dataset_sentiment
dataset_sentiment = "trust";

# read file
myfile = open("twitter_message/dataset_dt_" + dataset_sentiment + "_60k.txt", "rt", encoding='utf-8')
contents = myfile.read()
myfile.close()

# i = 0

for line in contents.splitlines():
    # 1. remove URL and USERNAME
    line = remove_url_and_username(line)
    # print(line)

    # 2. process hash-tag: collect hash-tag(#) (list)
    line = process_h(line)

    # 3. process emoji and emoticons (list)
    line = process_emoji_and_emoticons(line)

    # 4. treatment punctuation marks and substitution with spaces
    line = treatment_punctuation(line)

    # 5. transformation to lower case

    # 6. sentence tokenisation

    # 7. process slang word and acronyms (list)

    # 8. POS tagging

    # 9. lemmatization

    # 10. stop words elimination

    # 11. stem frequency counting (for each word)
    # fdist = nltk.FreqDist(words_without_stopwords).most_common()


