#pip list:
#
# tensorflow             2.3.0

#https://keras.io/examples/nlp/text_classification_with_transformer/
#https://androidkt.com/text-classification-using-attention-mechanism-in-keras/
#https://www.tensorflow.org/api_docs/python/tf/keras/layers/Attention

import tensorflow as tf
import keras
from keras_preprocessing import sequence
import numpy as np
from sklearn.model_selection import train_test_split

from spam_dataset import SpamDataset
from layers import *

def main():
    n_words = 10000
    embedding_dim = 50
    max_len = 50 #only take top 50 words


    X, y = SpamDataset.get_data()

    #tokenize
    tokenizer = keras.preprocessing.text.Tokenizer(num_words=n_words, split=' ')
    tokenizer.fit_on_texts(X)
    X = tokenizer.texts_to_sequences(X)

    #pad sequences
    X = sequence.pad_sequences(X, maxlen=max_len, truncating='post', padding='post', value=0)
    
    X = np.array([np.array(x).astype('float32') for x in X])
    y = np.array(y).astype('float32')

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    embed_dim = 32
    num_heads = 1

    transformer_layer = TransformerBlock(embed_dim, num_heads, 50)
    embedding_layer = TokenAndPositionEmbedding(max_len, n_words, embed_dim)

    input_layer = layers.Input(shape=(max_len,))
    layer_embed = embedding_layer(input_layer)
    layer_trans = transformer_layer(layer_embed)
    layer_gap = layers.GlobalAveragePooling1D()(layer_trans)
    layer_den = layers.Dense(20, activation="relu")(layer_gap)
    output_layer = layers.Dense(2, activation="softmax")(layer_den)

    model = keras.Model(inputs=input_layer, outputs=output_layer)

    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

    model.summary()
    
    model.fit(X_train, y_train, epochs=4)

    model.evaluate(X_test, y_test)

    print()

if __name__ == "__main__":
    main()
