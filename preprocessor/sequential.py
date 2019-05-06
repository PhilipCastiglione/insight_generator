import os
import time

from dotenv import load_dotenv
from google.cloud import storage
import pandas as pd
# import spacy # TODO: do I need this?
from spacy.lang.en import English
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')

# TODO: we might not use this approach for getting creds on our cloud instance
load_dotenv(verbose=True)

timestamp = str(int(time.time()))

print("Beginning sequential preprocessing task: {}".format(timestamp))

storage_client = storage.Client()
bucket_name = os.getenv("GCP_BUCKET_NAME")
storage_prefix = "{}/sequential/{}/".format(BUCKET_NAME, timestamp)
source_data_url = ""
source_filename = "source.csv"
source_path = storage_prefix + source_filename

# TODO: call external service; stream download of file into bucket

print("...Downloaded and stored data at: {}".format(source_path))

# TODO: access source from storage
# TODO: use a streaming approach...

linebreaks = re.compile(r"[\n\r]")

def replace_linebreaks(comment):
    comment = linebreaks.sub(' ', comment)
    comment = comment.lower()
    return comment

def filter_nonstring_comments(comment):
    return type(comment) == str

source_rows = pd.read_csv(
    ...,
    dtype={
        'listing_id': 'str',
        'id': 'str',
        'comments': 'str',
    })

cleaned_rows = source_rows[source_rows['comments'].apply(filter_comments)]
cleaned_rows = cleaned_rows['comments'].apply(replace_linebreaks)
cleaned_rows.to_csv(..., columns=['comments'], line_terminator='\n', index=False, header=False)

cleaned_corpus_filename = "cleaned_corpus.csv"
cleaned_corpus_path = storage_prefix + cleaned_corpus_filename

# TODO: store back in cloud storage

print("...Cleaned and stored corpus at: {}".format(cleaned_corpus_path))

# TODO: access cleaned corpus from storage
# TODO: use a streaming approach...

tokenizer = English()
lemmatizer = WordNetLemmatizer()
en_stop = set(nltk.corpus.stopwords.words('english'))

def tokenize(document):
    lda_tokens = []
    tokens = tokenizer(document)
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

cleaned_documents = pd.read_csv(
    ...,
    )

preprocessed_documents = [preprocess(document) for document in cleaned_documents]

preprocessed_corpus_filename = "preprocessed_corpus.csv"
preprocessed_corpus_path = storage_prefix + preprocessed_corpus_filename

# TODO: store back in cloud storage

print("...Preprocessed and stored documents at: {}".format(preprocessed_corpus_path))

print("Completed sequential preprocessing task: {}".format(timestamp))

print("Time taken: {}".format(timestamp - str(int(time.time()))))

