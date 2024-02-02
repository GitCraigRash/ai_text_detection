# -*- coding: utf-8 -*-
"""Experimental_ai_text_detector.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15cqVxlqnm9QfNqqiFJL3CNeRT4oMX4zi

ai_generated_text detection
"""

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

df["text"]= df["text"].apply(lambda x: x.lower())

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

import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Define maximum sequence length
max_sequence_length = 2000

# Tokenize the text and pad sequences
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(df['text'])
df_seq = tokenizer.texts_to_sequences(df['text'])
df_padded = pad_sequences(df_seq, maxlen=max_sequence_length)



### CHAT CREATe NEW AXIS
import numpy as np

# Example array
original_array = np.array([1, 2, 3, 4, 5])

# Add a new axis to the array
new_dimension_array = original_array[:, np.newaxis]

# Check the shape of the new array
print("Original array shape:", original_array.shape)
print("New array shape:", new_dimension_array.shape)

import numpy as np

# Example array
original_array = np.array([1, 2, 3, 4, 5])

# Add a new dimension to the array
new_dimension_array = np.expand_dims(original_array, axis=1)

# Check the shape of the new array
print("Original array shape:", original_array.shape)
print("New array shape:", new_dimension_array.shape)

mask = np.random.choice([True, False], size=len(df), p=[0.8, 0.2])

# Split the data based on the mask
X_train = df_padded[:[mask]]
y_train = df_padded[:[~mask]]
X_test = df_padded[mask]
y_test = df_padded[~mask]

df_padded = None

X_train.head(),len(y_train),X_test.head(),len(y_test)

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
        np.random.shuffle(indices)
        for start in range(0, num_samples, batch_size):
            end = min(start + batch_size, num_samples)
            batch_indices = indices[start:end]

            x_batch = x_data[batch_indices]
            y_batch = y_data[batch_indices]

            yield x_batch, y_batch

        # Housekeeping
        gc.collect()
        tf.keras.backend.clear_session()


my_training_batch_generator = data_generator(X_train_padded, y_train, batch_size)
my_validation_batch_generator = data_generator(X_test, y_test, batch_size)

# Define the model
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index)+1, output_dim=64, input_length=max_sequence_length),
    LSTM(64),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(my_training_batch_generator, df["label"], epochs=1, batch_size=20, validation_data=EvalCallback)

# Save the model
model.save('lstm_model.h5')





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