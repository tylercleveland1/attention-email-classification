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

        self.CONST_ATTENTION_FILTER = 0.1

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
        self.embedding_layer = embedding_layer

    def get_prediction_and_data(self, email_text):
        x_input = self.tokenizer.texts_to_sequences([
            email_text
        ])
        
        x_input = sequence.pad_sequences(x_input, maxlen=self.max_len, truncating='post', padding='post', value=0)

        att_layer_values = np.array(self.model_satt(x_input))
        emb_layer_values = np.array(self.model_emb(x_input))
        prediction = np.array(self.model(x_input))
        att_scores = att_layer_values - emb_layer_values

        #sum per token
        att_scores_per_token = np.array([np.average(arr, axis=1) for arr in att_scores])
        #normalize over rows (sklearn.preprocessing.normalize)
        att_scores_per_token = normalize(att_scores_per_token)

        tokens = self.reverse_token_emb(emb_layer_values)

        reverse_word_index = {y:x for x,y in self.tokenizer.word_index.items()}

        token_att_scores = []
        #len(tokens) == len(att_scores_per_token)
        for i in range(len(tokens)):
            #zip the att scores and tokens together for each word
            token_att_scores.append(
                np.array(
                    list(zip(tokens[i], att_scores_per_token[i]))
                )
            )

        token_att_scores = np.array(token_att_scores)

        print(token_att_scores.shape)
        word_list = []
        for item in token_att_scores:
            for pair in item:
                if (reverse_word_index.get(pair[0], None) != None):
                    word_list.append((reverse_word_index[pair[0]], pair[1]))
        
        # word_list.sort()
        keywords = sorted(word_list, key=lambda x: x[1], reverse=True)
        
        out_dict = {}

        out_dict['keywords'] = filter(lambda x: x[1] > self.CONST_ATTENTION_FILTER, keywords)
        out_dict['prediction'] = self.one_hot_decode(prediction)

        return out_dict

    ## utilities
    def reverse_token_emb(self, X):
        X = np.array(X)
        lookup_dict = {}
        
        token_emb_weights = self.embedding_layer.get_weights()[0]
        texts = []
        for word in X:
            text_word_idxs = []
            for embed_vec in word:
                tuple_embed_vec = tuple(embed_vec)
                
                #if lookup dict contains embedded vector use it
                if lookup_dict.get(tuple_embed_vec, None) != None:
                    text_word_idxs.append(lookup_dict[tuple_embed_vec])
                #else search for embedding and cache it
                else:
                    for idx in range(token_emb_weights.shape[0]):
                        if np.array_equal(embed_vec, token_emb_weights[idx]):
                            lookup_dict[tuple_embed_vec] = idx
                            text_word_idxs.append(idx)
                        
            texts.append(text_word_idxs)
        
        return np.array(texts)

    def one_hot_decode(self, Y):
        Y = np.array(Y)
        Y = np.eye(Y.shape[1])[Y.argmax(1)]
        return np.array(["spam" if y[1] == 1 else "ham" for y in Y])