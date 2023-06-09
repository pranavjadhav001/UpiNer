import spacy
import argparse
import os

class SpacyInfer:
    def __init__(self,model_dir):
        if not os.path.exists(model_dir):
            raise OSError('model dir does not exists')
        self.nlp_ner = spacy.load(model_dir)

    def ner_infer(self,text):
        doc_dict = dict()
        doc = self.nlp_ner(text)
        for ent in doc.ents:
            if ent.label_ in doc_dict:
                doc_dict[ent.label_].append(ent.text)
            else:
                doc_dict[ent.label_] = [ent.text]
        return doc_dict
