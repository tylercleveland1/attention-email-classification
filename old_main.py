#pip list:
#
# tensorflow             2.3.0

#https://keras.io/examples/nlp/text_classification_with_transformer/
#https://androidkt.com/text-classification-using-attention-mechanism-in-keras/
#https://www.tensorflow.org/api_docs/python/tf/keras/layers/Attention

#https://stackoverflow.com/questions/51235118/how-to-get-word-vectors-from-keras-embedding-layer

import tensorflow as tf
import keras
from keras_preprocessing import sequence
import numpy as np
from sklearn.model_selection import train_test_split

from spam_dataset import SpamDataset
from layers import *

def main():
    n_words = 10000
    max_len = 50 #only take top 50 words

    embed_dim = 32
    num_heads = 1

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

    l_input = layers.Input(shape=(max_len,))
    l_embedding = TokenAndPositionEmbedding(max_len, n_words, embed_dim)(l_input)

    l_mha = SelfAttention(embed_dim)(l_embedding)
    l_pool = layers.GlobalAveragePooling1D()(l_mha)
    l_output = layers.Dense(2, activation="softmax")(l_pool)
    
    model = keras.Model(inputs=l_input, outputs=l_output)
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
    model.summary()
    
    model.fit(X_train, y_train, epochs=4)

    model.evaluate(X_test, y_test)


    #get intermediate layer
    model_emb = keras.Model(input=l_input, output=l_embedding)
    #test inputs
    x_pred = tokenizer.texts_to_sequences(["this is a test of the email classification system"]);
    x_pred = sequence.pad_sequences(x_pred, maxlen=max_len, truncating='post', padding='post', value=0)
    print(
        model_emb.predict(x_pred)
    )

if __name__ == "__main__":
    main()
