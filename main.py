#pip list:
#
# tensorflow             2.3.0

#https://keras.io/examples/nlp/text_classification_with_transformer/
#https://androidkt.com/text-classification-using-attention-mechanism-in-keras/
#https://www.tensorflow.org/api_docs/python/tf/keras/layers/Attention

from spam_dataset import SpamDataset
import tensorflow as tf
from keras_preprocessing import sequence

def main():
    n_words = 10000
    embedding_dim = 50
    max_len = 250


    X, y = SpamDataset.get_data()

    #tokenize
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=n_words, split=' ')
    tokenizer.fit_on_texts(X)
    X = tokenizer.texts_to_sequences(X)

    #pad sequences
    X = sequence.pad_sequences(X, maxlen=max_len, truncating='post', padding='post', value=0)

    #create model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Embedding(n_words, embedding_dim, input_length = X.shape[1]))

    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)


if __name__ == "__main__":
    main()
