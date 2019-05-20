import argparse

import pandas as pd
from spacy.lang.en import English
import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

tokenizer = English()
lemmatizer = WordNetLemmatizer()
en_stop = set(nltk.corpus.stopwords.words('english'))

def tokenize(document):
    lda_tokens = []
    tokens = tokenizer(str(document))
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma(word):
    lemma = wordnet.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def get_lemma2(word):
    return lemmatizer.lemmatize(word)

def preprocess(document):
    tokens = tokenize(document)
    tokens = [token for token in tokens if len(token) >= 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    tokens = [get_lemma2(token) for token in tokens]
    return tokens

parser = argparse.ArgumentParser()
parser.add_argument('input', help='path to input file')
parser.add_argument('output', help='path to output file')
args = parser.parse_args()

source_rows = pd.read_csv(
    args.input,
    names=['comments'],
    header=None,
    dtype={ 'comments': 'str' })

preprocessed_rows = source_rows['comments'].apply(preprocess)
preprocessed_rows.to_csv(args.output, columns=['comments'], line_terminator='\n', index=False, header=False)

