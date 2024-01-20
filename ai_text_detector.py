# -*- coding: utf-8 -*-
"""ai_text_detector.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uJJgGipJBP9fLv3l3rTt_5IXpOhyIk4E

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

def tf_lower_and_strip(text):
    text = tf_text.normalize_utf8(text, 'NFKD')
    text = tf.strings.lower(text)
    text = tf.strings.strip(text)
    text = tf.strings.join(['[START]', text, '[END]'], separator=' ')
    return text

#df["text"]= df["text"].apply(lambda x: x.encode('utf-8').decode('utf-8'))
#df["text"]= df["text"].apply(lambda x: re.sub("\n",' ', x))
#df["text"]= df["text"].apply(lambda x: re.sub('\s+',' ', x))
#print(df["text"].head())

# for the first try, we will avoid eliminating special characters.
# We believe this will help us differentiant betweeen students and AI.



#vectorize
vectorize_layer = tf.keras.layers.TextVectorization(
    standardize=tf_lower_and_strip,
    max_tokens=75000,
    ngrams = (3,5),
    output_mode="int",
    output_sequence_length=512,
    pad_to_max_tokens=True
    )





