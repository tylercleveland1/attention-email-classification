import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import re

class SpamDataset:
    puncutation_stops = ['!', '@', '#']
    #Returns (X_train, y_train, X_test, y_test), for SpamDataset
    @staticmethod
    def get_train_test_data():
        #load emails csv
        ds_emails = pd.read_csv('./data/emails.csv')
        texts = ds_emails['text'].apply(SpamDataset.__clean_text)
        classes = ds_emails['spam']
        
        return train_test_split(texts, classes, test_size=0.25)

    @staticmethod
    def __clean_text(text):
        #remove prefix of 'Subject: '
        text = text[8:]
        #remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        #remove extra whitespace
        text = ' '.join(text.split())
        return text