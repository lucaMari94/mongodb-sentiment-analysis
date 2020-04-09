# 7. process slang word and acronyms (list)
prova = ['afaik', 'ciao', 'simone', 'wtg']
prova = replace_slang(prova)
print(prova)

test = ['when', 'english', 'what']
stop_words = set(stopwords.words('english'))
filtered_sentence = [word for word in test if not word in stop_words]