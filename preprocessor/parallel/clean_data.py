import argparse
import re

import pandas as pd

def filter_nonstring_comments(comment):
    return type(comment) == str

linebreak_regex = re.compile(r"[\n\r]")
def replace_linebreaks(comment):
    comment = linebreak_regex.sub(' ', comment)
    comment = comment.lower()
    return comment

parser = argparse.ArgumentParser()
parser.add_argument('input', help='path to input file')
parser.add_argument('output', help='path to output file')
args = parser.parse_args()

source_rows = pd.read_csv(
    args.input,
    dtype={
        'listing_id': 'str',
        'id': 'str',
        'comments': 'str',
    })

cleaned_rows = source_rows[source_rows['comments'].apply(filter_nonstring_comments)]
cleaned_rows = cleaned_rows['comments'].apply(replace_linebreaks)
cleaned_rows.to_csv(args.output, columns=['comments'], line_terminator='\n', index=False, header=False)

