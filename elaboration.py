from config import slang_words, posemoticons, negemoticons, other_emoticons, \
    EmojiPos, EmojiNeg, OthersEmoji, AdditionalEmoji, MyEmoji

# 1. remove URL and USERNAME (anonymization)
def remove_url_and_username(line):
    line = line.replace('URL', '')
    line = line.replace('USERNAME', '')
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
    print(line)
    # 2. process hash-tag: collect hash-tag(#) (list)

    # 3. process emoji and emoticons (list)

    # 4. treatment punctuation marks and substitution with spaces
    # [,?!.;:\/()& _+=<>"]

    # 5. transformation to lower case

    # 6. sentence tokenisation

    # 7. process slang word and acronyms (list)

    # 8. POS tagging

    # 9. lemmatization

    # 10. stop words elimination

    # 11. stem frequency counting (for each word)
    # fdist = nltk.FreqDist(words_without_stopwords).most_common()


