from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

import unicodedata
import re
import numpy as np
import os
import io
import time
import json
from tensorflow.keras import preprocessing
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense, concatenate


WORD_DICT_SIZE = 50002
POS_DICT_SIZE = 53
DEP_DICT_SIZE = 54
WORD_EMB_DIM = 128
POS_EMB_DIM = 128
DEP_EMB_DIM = 128
NUM_UNITS = 100
NUM_LAYERS = 1

# Encoder
class Encoder(tf.keras.Model):
  def __init__(self, vocab_size, enc_units, batch_sz):
    super(Encoder, self).__init__()
    self.batch_sz = batch_sz
    self.enc_units = enc_units
    self.word_embedding = Embedding(WORD_DICT_SIZE, WORD_EMB_DIM, mask_zero=True, embeddings_initializer='glorot_uniform')
    self.pos_embedding = Embedding(POS_DICT_SIZE, POS_EMB_DIM, mask_zero=True, embeddings_initializer='glorot_uniform')
    self.dep_embedding = Embedding(DEP_DICT_SIZE, DEP_EMB_DIM, mask_zero=True, embeddings_initializer='glorot_uniform')
    self.lstm = LSTM(NUM_UNITS, return_sequences=True, return_state=True, dropout=0.5, recurrent_initializer='glorot_uniform')
    self.bidirectional = Bidirectional(self.lstm, merge_mode='concat')
    self.fc = Dense(1, activation='sigmoid')

  def call(self, words, pos, dep):
    word_emb = self.word_embedding(words)
    pos_emb = self.pos_embedding(pos)
    dep_emb = self.dep_embedding(dep)
    mask = self.dep_embedding.compute_mask(words)
    x = concatenate([word_emb, pos_emb, dep_emb])
    x, forward_ouput, forward_state, backward_output, backward_state = self.bidirectional(x, mask=mask)
    output = tf.squeeze(self.fc(x), -1)
    return output


def evaluate(encoder, words, pos, dep):
  word_seq = tf.dtypes.cast(tf.convert_to_tensor(words), dtype=tf.dtypes.float32)
  pos_seq = tf.dtypes.cast(tf.convert_to_tensor(pos), dtype=tf.dtypes.float32)
  dep_seq = tf.dtypes.cast(tf.convert_to_tensor(dep), dtype=tf.dtypes.float32)

  enc_out = encoder(word_seq, pos_seq, dep_seq)

  return(enc_out)

