# -*- coding: utf-8 -*-
"""Experimental_ai_text_detector.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15cqVxlqnm9QfNqqiFJL3CNeRT4oMX4zi

ai_generated_text detection
"""

my_dict = {'a': 1, 'b': 2, 'c': 3}

all_entries_except_first = list(my_dict.items())[1:]

print(all_entries_except_first[0][0])

#ai_generated_text_detection

import pandas as pd
import numpy as np

from google.colab import drive
drive.mount('/content/drive')

training_dir = '/content/drive/MyDrive/ai_text_detection/final_train.csv'
df = pd.read_csv(training_dir)

df.columns, df.shape

testing_dir = '/content/drive/MyDrive/ai_text_detection/final_test.csv'
test_df = pd.read_csv(testing_dir)

#Limit DataFrames for prototyping purposes.
df=df[:100]
test_df=test_df[:100]
test_df.columns, test_df.shape

import os
import random
import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import re
import string
#import tensorflow_text as tf_text

df["text"] = df["text"].apply(lambda x: x.lower())

df["text"].head()

df["label"].head()

def tf_lower_and_strip(text):
    text = text.normalize_utf8(text, 'NFKD')
    text = tf.strings.lower(text)
    text = tf.strings.strip(text)
    text = tf.strings.join(['[START]', text, '[END]'], separator=' ')
    return text

#df["text"]= df["text"].apply(lambda x: x.encode('utf-8').decode('utf-8'))
#df["text"]= df["text"].apply(lambda x: re.sub("\n",' ', x))
#df["text"]= df["text"].apply(lambda x: re.sub('\s+',' ', x))
#print(df["text"].head())

# for the first try, we will avoid eliminating special characters.
# We believe this will help us differentiant betweeen students and AI by catching punctuation errors.

df['text'] = df['text'].apply(lambda x: x.strip())
df["text"] = df["text"].apply(lambda x: re.sub("\n",' ', x))
df["text"] = df["text"].apply(lambda x: re.sub('\s+',' ', x))
print(df['text'].head())

test_df['text'] = test_df['text'].apply(lambda x: x.strip())
test_df["text"] = test_df["text"].apply(lambda x: re.sub("\n",' ', x))
test_df["text"] = test_df["text"].apply(lambda x: re.sub('\s+',' ', x))
print(df['text'].head())

import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Define maximum sequence length
max_sequence_length = 500

# Tokenize the text and pad sequences
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(df['text'])
df_seq = tokenizer.texts_to_sequences(df['text'])
df_padded = pad_sequences(df_seq, maxlen=max_sequence_length)

df_padded=pd.DataFrame(df_padded)
mask = list(np.random.choice([True, False], size=len(df), p=[0.8, 0.2]))
df_padded["mask"] = mask
df["mask"] = mask
# Split the data based on the mask
X_train = df_padded.loc[df_padded["mask"]==True]
y_train = df["label"].loc[df["mask"]==True]
#X_train = np.array(X_train)
#X_test = np.array(X_test)

X_test = df_padded.loc[df_padded["mask"]==False]
y_test = df["label"].loc[df["mask"]==False]
#y_train = np.array(y_train)
#y_test = np.array(y_test)
X_train = X_train.drop(columns=['mask'])
y_train = y_train.drop(columns=['mask'])
X_test = X_test.drop(columns=['mask'])
y_test = y_test.drop(columns=['mask'])

X_train=X_train.values
y_train=y_train.values
X_test=X_test.values
y_test=y_test.values



y_train=y_train.reshape(-1, 1)
y_test=y_test.reshape(-1, 1)

y_train.shape,y_train

#Create Baseline
unique_elements,counts=np.unique(y_test,return_counts=True)
counts[0]/len(y_test)

pip install -q -U keras-tuner

import keras_tuner

def model_builder(hp):
  model = keras.Sequential()
  model.add(keras.layers.Flatten(input_shape=(28, 28)))

  # Tune the number of units in the first Dense layer
  # Choose an optimal value between 32-512
  hp_units = hp.Int('units', min_value=32, max_value=512, step=32)
  model.add(keras.layers.Dense(units=hp_units, activation='relu'))
  model.add(keras.layers.Dense(10))

  # Tune the learning rate for the optimizer
  # Choose an optimal value from 0.01, 0.001, or 0.0001
  hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])

  model.compile(optimizer=keras.optimizers.Adam(learning_rate=hp_learning_rate),
                loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

  return model

import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
import gc
from keras.utils import Sequence
from tensorflow.keras.callbacks import Callback

batch_size = 20

def data_generator(x_data, y_data, batch_size):
    num_samples = len(x_data)
    indices = np.arange(num_samples)

    while True:
        #np.random.shuffle(indices)
        for start in range(0, num_samples, batch_size):
            end = min(start + batch_size, num_samples)
            batch_indices = indices[start:end]
            print(batch_indices)
            x_batch = x_data[batch_indices]
            y_batch = y_data[batch_indices]
            yield x_batch, y_batch

        # Housekeeping
        gc.collect()
        tf.keras.backend.clear_session()


my_training_batch_generator = data_generator(X_train, y_train, batch_size)
my_validation_batch_generator = data_generator(X_test, y_test, batch_size)

import tensorflow as tf

# Define the vocabulary size and embedding dimension
vocab_size = len(tokenizer.word_index) + 1

# Define the model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=10, input_length=500),
    #tf.keras.layers.Dense(1000, activation='softmax'),
    tf.keras.layers.LSTM(units=100,return_sequences=False),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print the model summary
model.summary()

# Train the model
model.fit(X_train,y_train, epochs=3, batch_size=20)

# Save the model
model.save('lstm_model.h5')

test_loss, test_acc = model.evaluate(X_test, y_test)
print("Test accuracy:", test_acc)

predicted_labels = model.predict(X_test)
predicted_labels = predicted_labels.flatten()
binary_predictions = (predicted_labels > 0.5).astype(int)
y_test,binary_predictions

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, binary_predictions)
# Visualize confusion matrix
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
plt.xlabel('Predicted Label')
plt.ylabel('True Label')

# Add annotations
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, str(cm[i, j]), ha='center', va='center', color='white' if cm[i, j] > np.max(cm) / 2 else 'black')

# Set class labels
classes = ['Class 0', 'Class 1']
plt.xticks(np.arange(len(classes)), classes)
plt.yticks(np.arange(len(classes)), classes)

plt.show()

#What words were misclassfiied?

word_index = tokenizer.word_index
word_index

type(word_index),len(word_index)

!pip install pyldavis

binary_predictions = binary_predictions.reshape(-1, 1)
#type(y_test),type(binary_predictions),type(word_index)
y_test.shape, binary_predictions.shape #word_index.shape
X_test.shape

type(X_test),len(X_test)

type(y_test),len(y_test)
X_test



def unique_words(X_test,y_test,binary_predictions,word_index):
  """
  Take the most common unique words from each category
  and return them as a DataFrame sorted by frequency
  """
  #loop through each paragraph recording the number of times a word appears
  # create dictionary for each class,
  # count word frequency in a loop ignore 0
  # convert to dataframe and return
dic_0 = {}
dic_1 = {}
def update_dictionary(dictionary, key):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def invert_dictionary(dictionary):
    inverted_dict = {value: key for key, value in dictionary.items()}
    return inverted_dict


def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None


inv_word_index = invert_dictionary(word_index)
for i,k in enumerate(X_test):
  if y_test[i] == 0:
    for j in k:
      if j != 0:
        update_dictionary(dic_0, inv_word_index[j])
    continue
  for j in k:
    if j != 0:
      update_dictionary(dic_1, inv_word_index[j])

dic_1=pd.DataFrame(dic_1.values(),dic_1.keys())
dic_0=pd.DataFrame(dic_0.values(),dic_0.keys())

dic_1 = dic_1.sort_values(by=0, ascending=False)
dic_0 = dic_0.sort_values(by=0, ascending=False)

dic_1 = dic_1.transpose()
dic_0 = dic_0.transpose()

dic_1,dic_0

# what words are unique to both?
def unique_words(dic_0,dic_1):
  #add words in dic_0 not found in dic_1
  unshared_words = []
  for i in dic_0.columns:
    if i in dic_1.columns:
      continue
    unshared_words.append(dic_0[i])
  return unshared_words

print(unique_words(dic_1,dic_0))

true_positive_tokens = []
false_positive_tokens = []
true_negative_tokens = []
false_negative_tokens = []

for i in range(len(X_test)):
        true_label=y_test[i]
        predicted_label=binary_predictions[i]
        if true_label == 1 and predicted_label == 1:  # True Positive
            true_positive_tokens.append(i)
        elif true_label == 0 and predicted_label == 1:  # False Positive
            false_positive_tokens.append(i)
        elif true_label == 0 and predicted_label == 0:  # True Negative
            true_negative_tokens.append(i)
        elif true_label == 1 and predicted_label == 0:  # False Negative
            false_negative_tokens.append(i)

# Example print statements to show the tokens in each category
print("True Positive Tokens:", true_positive_tokens[:10])  # Print first 10 tokens for illustration
print("False Positive Tokens:", false_positive_tokens[:10])  # Print first 10 tokens for illustration
print("True Negative Tokens:", true_negative_tokens[:10])  # Print first 10 tokens for illustration
print("False Negative Tokens:", false_negative_tokens[:10])  # Print first 10 tokens for illustration

reversed_dict = {v: k for k, v in word_index.items()}

tp_word_counts["410"] += 1
tp_word_counts

tp_word_counts

tp_word_counts = {}
fp_word_counts = {}
tn_word_counts = {}
fn_word_counts = {}

for i in true_positive_tokens:
  for token in X_train[i]:
      print(token)
      while token !=0:
        while tp_word_counts.get(token):
          tp_word_counts[token] += 1
          continue
        tp_word_counts[token] = 1
        continue
      continue

# Update word counts for False Positive Tokens
for i in false_positive_tokens:
    for token in X_test[i]:
        fp_word_counts[token] += 1

# Update word counts for True Negative Tokens
for i in true_negative_tokens:
    for token in X_test[i]:
        tn_word_counts[token] += 1

# Update word counts for False Negative Tokens
for i in false_negative_tokens:
    for token in X_test[i]:
        fn_word_counts[token] += 1

print("True Positive Word Counts:", dict(list(tp_word_counts.items())[:10]))
print("False Positive Word Counts:", dict(list(fp_word_counts.items())[:10]))
print("True Negative Word Counts:", dict(list(tn_word_counts.items())[:10]))
print("False Negative Word Counts:", dict(list(fn_word_counts.items())[:10]))

#toy example
x_train = [random.randint(1, 100) for _ in range(100)]  # Generates a list of 10 random integers between 1 and 100
y_train = [random.randint(1, 100) for _ in range(100)]  # Generates a list of 10 random integers between 1 and 100

my_training_batch_generator(x_train,y_train,5)

import pandas as pd
import numpy as np
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Input, Dense, GRU, Embedding, LSTM, Flatten
from tensorflow.python.keras.optimizers import RMSprop
from tensorflow.python.keras.callbacks import EarlyStopping
ModelCheckpoint, TensorBoard, ReduceLROnPlateau


batch_size = 500
feature_no = 13
period_no = 8640
def gen(batch_size, periods):
  j = 0
  features = ['ask_close',
              'ask_open',
              'ask_high',
              'ask_low',
              'bid_close',
              'bid_open',
              'bid_high',
              'bid_low',
              'open',
              'high',
              'low',
              'close',
              'price']
  with pd.HDFStore('datasets/eurusd.h5') as store:
      df = store['train_buy']

  x_shape = (batch_size, periods, len(features))
  x_batch = np.zeros(shape = x_shape, dtype=np.float16)

  y_shape = (batch_size, periods)
  y_batch = np.zeros(shape = y_shape, dtype=np.float16)

  while True:
      i = 0
      while len(x_batch) < batch_size:
          if df.iloc[j+periods]['direction'].values == 1:
              x_batch[i] = df.iloc[j:j+periods][features].values.tolist()
              y_batch[i] = df.iloc[j+periods]['target_buy'][0].round(4)
              i+=1
          j+=1
          if j == 56241737 - periods:
              j = 0
      yield x_batch, y_batch

generator = gen(batch_size, period_no)

model = Sequential()
model.add(LSTM(units = 1, return_sequences=True, input_shape = (None, feature_no,)))


optimizer = RMSprop(lr=1e-3)
model.compile(loss = 'mse', optimizer = optimizer)
model.fit_generator(generator=generator, epochs = 10, steps_per_epoch = 112483)

### Alternate method using custom partitioning and .fit_generator()
import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, data, labels, batch_size=20, dim=len(tokenizer.word_index)+1,
                 n_classes=10, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.data = data
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.data) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        data_temp = [self.data[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(data_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arrange(len(self.data))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples'
        # Initialization
        X = np.empty((self.batch_size, *self.dim))
        y = np.empty((self.batch_size), dtype=int)

        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            X[i,] = np.load('data/' + ID + '.npy')

            # Store class
            y[i] = self.labels[ID]

        return X, keras.utils.to_categorical(y, num_classes=self.n_classes)

import numpy as np

from keras.models import Sequential
from my_classes import DataGenerator

# Parameters
params = {'dim': (1),
          'batch_size': 20,
          'n_classes': 1,
          'n_channels': 1,
          'shuffle': True}

# Datasets
partition = # IDs
labels = # Labels

# Generators
training_generator = DataGenerator(partition['train'], labels, **params)
validation_generator = DataGenerator(partition['validation'], labels, **params)

# Design model
model = Sequential()
[...] # Architecture
model.compile()

# Train model on dataset
model.fit_generator(generator=training_generator,
                    validation_data=validation_generator,
                    use_multiprocessing=True,
                    workers=6)



#vectorize
# Standardize each example (usually lowercasing + punctuation stripping)
# Split each example into substrings (usually words)
# Recombine substrings into tokens (usually ngrams)
# Index tokens (associate a unique int value with each token)
# Transform each example using this index, either into a vector of ints or a dense float vector.

# TextVectorization is non-trainable! Its state is not set during training;
# it must be set BEFORE training, either by initializing it from a precomputed constant,
# or by "adapting" it on data. .adapt()

# Example of adapt()
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten

data = [
    "ξεῖν᾽, ἦ τοι μὲν ὄνειροι ἀμήχανοι ἀκριτόμυθοι",
    "γίγνοντ᾽, οὐδέ τι πάντα τελείεται ἀνθρώποισι.",
    "δοιαὶ γάρ τε πύλαι ἀμενηνῶν εἰσὶν ὀνείρων:",
    "αἱ μὲν γὰρ κεράεσσι τετεύχαται, αἱ δ᾽ ἐλέφαντι:",
    "τῶν οἳ μέν κ᾽ ἔλθωσι διὰ πριστοῦ ἐλέφαντος,",
    "οἵ ῥ᾽ ἐλεφαίρονται, ἔπε᾽ ἀκράαντα φέροντες:",
    "οἱ δὲ διὰ ξεστῶν κεράων ἔλθωσι θύραζε,",
    "οἵ ῥ᾽ ἔτυμα κραίνουσι, βροτῶν ὅτε κέν τις ἴδηται.",
]
layer = layers.TextVectorization()
layer.adapt(data)
vectorized_text = layer(data)
print(vectorized_text)

# vectorized_text output
"""tf.Tensor(
[[37 12 25  5  9 20 21  0  0]
 [51 34 27 33 29 18  0  0  0]
 [49 52 30 31 19 46 10  0  0]
 [ 7  5 50 43 28  7 47 17  0]
 [24 35 39 40  3  6 32 16  0]
 [ 4  2 15 14 22 23  0  0  0]
 [36 48  6 38 42  3 45  0  0]
 [ 4  2 13 41 53  8 44 26 11]], shape=(8, 9), dtype=int64)"""

vectorize_layer = tf.keras.layers.TextVectorization(
    standardize=tf_lower_and_strip,
    max_tokens=75000,
    ngrams = (3,5),
    output_mode="int",
    output_sequence_length=512,
    pad_to_max_tokens=True
    )

layer = layers.TextVectorization()
layer.adapt(df["text"].head())
vectorized_text = layer(df["text"].head())
print(vectorized_text)