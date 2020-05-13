import matplotlib.pyplot as plt

myfile = open("frequency.txt", "rt", encoding='utf-8')
contents = myfile.read()
myfile.close()

sizes = []

for line in contents.splitlines():
    array = line.split(":")

    if array[0].find("media"): # end
        sizes.append(array[1].strip(" "))

# print(sizes)
labels = "anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"
explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
plt.figure(figsize=(5,5))
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90, wedgeprops={'alpha':0.8})
plt.axis('equal')
plt.show()