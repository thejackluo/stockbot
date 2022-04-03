from numpy import append
import pandas as pd
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import spacy

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

def remove_emoji(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags 
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', str(text))

def space(comment):
    doc = nlp(comment)
    return " ".join([token.lemma_ for token in doc])

def clean(filepath):
    df = pd.read_csv(filepath, index_col=0)
    #tokenization
    df['cleaned_content'] = df['content'].str.replace('[^\w\s]','')
    df['cleaned_content'] = df['cleaned_content'].apply(lambda x: remove_emoji(x))
    df['cleaned_content'] = df['cleaned_content'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    stop = stopwords.words('english')
    df['cleaned_content'] = df['cleaned_content'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    df['cleaned_content'] = df['cleaned_content'].apply(space)
    df['cleaned_content'] = df['cleaned_content'].apply(lambda x: word_tokenize(x))
    #dictionify left
    df.to_csv(filepath)

