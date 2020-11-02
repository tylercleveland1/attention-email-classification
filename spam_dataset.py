import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import re

class SpamDataset:
    
    #Returns (X_train, y_train, X_test, y_test), for SpamDataset
    @staticmethod
    def get_data():
        #load emails csv
        ds_emails = pd.read_csv('./data/emails.csv')
        texts = ds_emails['text'].apply(SpamDataset.__clean_text)
        classes = ds_emails['spam']
        
        return texts, classes

    @staticmethod
    def __clean_text(text):
        #remove prefix of 'Subject: '
        text = text[8:]
        #remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        #remove extra whitespace
        text = ' '.join(text.split())
        return text