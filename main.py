#pip list:
#
# tensorflow             2.3.0

#https://keras.io/examples/nlp/text_classification_with_transformer/
#https://androidkt.com/text-classification-using-attention-mechanism-in-keras/
#https://www.tensorflow.org/api_docs/python/tf/keras/layers/Attention

from spam_dataset import SpamDataset

def main():
    X_train, X_test, y_train, y_test = SpamDataset.get_train_test_data()


if __name__ == "__main__":
    main()
