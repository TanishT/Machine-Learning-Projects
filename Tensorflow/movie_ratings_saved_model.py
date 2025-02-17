import tensorflow as td
from tensorflow import keras
import numpy as np

data = keras.datasets.imdb

(train_data, train_labels), (test_data, test_labels) = data.load_data(num_words=88000)

word_index = data.get_word_index() 

word_index = {k:(v+3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

rating_length = np.arange(len(train_data))
for i in range(len(train_data)):
	rating_length[i] = len(train_data[i])

largest_rating = 0
for i in range(len(rating_length)):
	if rating_length[i] > largest_rating:
		largest_rating = rating_length[i]

def decode_review(text):
	return " ".join([reverse_word_index.get(i, "?") for i in text])

def review_enocde(s):
    encoded = [1]

    for word in s:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)
    
    return encoded

train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding="post", maxlen=largest_rating)
test_data = keras.preprocessing.sequence.pad_sequences(test_data, value=word_index["<PAD>"], padding="post", maxlen=largest_rating)

model = keras.models.load_model("savedModels/model.h5")

with open("Datasets/black.txt", encoding = "utf-8") as f:
    for line in f.readlines():
        nline = line.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(":", "").replace("\"", "").strip().split(" ")
        encode = review_enocde(nline)
        encode = keras.preprocessing.sequence.pad_sequences([encode], value=word_index["<PAD>"], padding="post", maxlen=largest_rating)
        predict = model.predict(encode)

        print(line)
        print(encode)
        print(predict[0])