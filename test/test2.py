from nltk import ngrams, FreqDist
all_counts = dict()

data = ["this", "is", 'this', 'is', 'simone', 'is']
fdist = FreqDist(data)
print(fdist.most_common())

###################################
frequency_array = [('simone', 2), ('really', 1), ('hot', 1)]
global_dict_count = {}
for element in frequency_array:
    # element[0] = word
    # element[1] = count

    # global_dict_count[element[0]] = element[1]

    if element[0] in global_dict_count.keys():
        global_dict_count[element[0]] = global_dict_count.get(element[0]) + 1
    else:
        global_dict_count[element[0]] = element[1]

print(global_dict_count)

# [('randomly', 1), ('get', 1), ('really', 1), ('hot', 1)]
# global_dict_count = { get:1, randomly:1 }

# [('randomly', 1), ('get', 2)]
# get: 1 + 2 = 3, randomly: 1 + 1 = 2