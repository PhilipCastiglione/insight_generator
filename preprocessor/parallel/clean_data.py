import argparse
import math
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
parser.add_argument('instance_number', type=int, help='the instance number of this vm')
parser.add_argument('scale', type=int, help='the total number of vms')
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

# we can now split exclusively the cleaned chunk out that this instance should preprocess
num_records = cleaned_rows.shape[0]
from_line = math.floor((args.instance_number) / args.scale * num_records)
up_to_line = math.floor((args.instance_number + 1) / args.scale * num_records)
cleaned_rows = cleaned_rows.iloc[from_line:up_to_line]

cleaned_rows.to_csv(args.output, columns=['comments'], line_terminator='\n', index=False, header=False)

