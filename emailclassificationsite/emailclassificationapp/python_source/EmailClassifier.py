#https://stackoverflow.com/questions/51235118/how-to-get-word-vectors-from-keras-embedding-layer

import tensorflow as tf
import keras
from keras_preprocessing import sequence
import numpy as np
from sklearn.preprocessing import normalize

from .Layers import SelfAttention

import pickle

import os

class EmailClassifier:
    def __init__(self):
        module_dir = os.path.dirname(__file__)

        self.model_hdf5_path = os.path.join(module_dir, 'self_attention_email_class.hdf5')
        self.tokenizer_pkl_path = os.path.join(module_dir, 'tokenizer.pkl')
        self.n_words = 10000
        self.max_len = 50 #only take top 50 words
        self.embed_dim = 32
        self.num_heads = 1

        with open(self.tokenizer_pkl_path, 'rb') as pickle_file:
            self.tokenizer = pickle.load(pickle_file)

        self.load_model()

    def load_model(self):
        l_input = keras.layers.Input(shape=(self.max_len,))
        embedding_layer = keras.layers.Embedding(input_dim=self.n_words, output_dim=self.embed_dim)
        l_embedding = embedding_layer(l_input)

        l_sa = SelfAttention(self.embed_dim)(l_embedding)
        l_pool = keras.layers.GlobalAveragePooling1D()(l_sa)
        l_output = keras.layers.Dense(2, activation="softmax")(l_pool)

        model = keras.Model(inputs=l_input, outputs=l_output)
        model.compile("adam", "categorical_crossentropy", metrics=["accuracy"])

        model.load_weights(self.model_hdf5_path)

        model_emb = keras.Model(inputs=l_input, outputs=l_embedding)
        model_satt = keras.Model(inputs=l_input, outputs=l_sa)

        self.model = model
        self.model_emb = model_emb
        self.model_satt = model_satt