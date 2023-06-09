
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
from spacy.util import filter_spans
import argparse
import pandas as pd
import json
import ast

nlp = spacy.blank("en") # load a new spacy model
doc_bin = DocBin() # create a DocBin object

parser = argparse.ArgumentParser()
parser.add_argument('--output_path',type=str,help='cuda or cpu')
parser.add_argument('--input_path',type=str,help='location to mvtec folder')
parser.add_argument('--input_type',type=str,help='type of input json/dataframe')
args = parser.parse_args()
if args.input_type == 'json':
    training_data = json.load(open(args.input_path,))
    for training_example in tqdm(training_data['annotations']):
        text = training_example[0]
        labels = training_example[1]['entities']
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in labels:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)
        filtered_ents = filter_spans(ents)
        doc.ents = filtered_ents
        doc_bin.add(doc)
elif args.input_type == "dataframe":
    df = pd.read_csv(args.input_path)
    for index,row in df.iterrows():
        text = row['text']
        labels = ast.literal_eval(row['entities'])
        doc = nlp.make_doc(text)
        ents = []
        print(labels)
        for start, end, label in labels:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)
        filtered_ents = filter_spans(ents)
        doc.ents = filtered_ents
        doc_bin.add(doc)

doc_bin.to_disk(args.output_path) # save the docbin object
