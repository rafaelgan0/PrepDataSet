import json
import pandas as pd
import spacy

def parse_review(text, id, score, reviewer_id):
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")
    # Process the text using spaCy
    doc = nlp(text)
    
    # Extract sentences from the processed text
    sentences = [sent.text for sent in doc.sents]
    json_list = []
    for sentence in sentences:
        json_obj = {
            "sentence": sentence,
            "id": id,
            "score": score,
            "reviewer_id": reviewer_id
        }
        json_list.append(json_obj)
    return json_list