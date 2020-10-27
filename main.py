#pip list:
#
# tensorflow             2.3.0

#https://keras.io/examples/nlp/text_classification_with_transformer/

from spam_dataset import SpamDataset

def main():
    X_train, X_test, y_train, y_test = SpamDataset.get_train_test_data()


if __name__ == "__main__":
    main()