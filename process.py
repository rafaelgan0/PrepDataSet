import pandas as pd
import json
from prompts import revise_review, label_review
from parser_module import parse_review
from ftfy import fix_encoding

fileName1 = 'C:\\Users\\rafae\\Documents\\PrepDataSet\\Data\\automatedAnnotations.jsonl'
fileName2 = "C:\\Users\\rafae\\Documents\\PrepDataSet\\Data\\manualAnnotations.jsonl"
outputFile = "C:\\Users\\rafae\\Documents\\PrepDataSet\\ProcessedDatasets\\dataset.csv"

identificationDf = pd.DataFrame(columns=['Prompt', 'Input', 'Output'])
revisionDf = pd.DataFrame(columns=['Prompt', 'Input', 'Output'])

# get manually annotated sentences
with open(fileName1, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(fix_encoding(line))
        sentences = data.get('sentences', [])

        for sentence in sentences:
            sentence_type = sentence.get('sentence_type', None)
            sentence = sentence.get('sentence', None)

            dataDf = pd.DataFrame({
                "Prompt": [label_review(sentence)],  # Assuming label_review returns a single value
                "Input": [sentence],
                "Output": [sentence_type]
            })

            # add data to the identification dataframe
            identificationDf = pd.concat([identificationDf, dataDf], ignore_index=True)

            ########## This part needs to be fixed ##########
            # add data to the revision dataframe
            # revisionDf.append({"Prompt": revise_review(sentence), "Sentence" : sentence, "Revision" : sentence_type})

# get automated annotations
with open(fileName2, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(fix_encoding(line))
        sentences = data.get('sentences', [])
        text = data.get('text', None)

        mapping = {
            "Confirmed" : 2,
            "Missed by Model" : 2,
            "Maybe" : 1,
            "Not concerning" : 0
        }

        entities = data.get('entities', [])

        for entity in entities:
            index1 = entity[0]
            index2 = entity[1]
            rating = entity[2]

            dataDf = pd.DataFrame({
                "Prompt": [label_review(sentence)], 
                "Input": [sentence],
                "Output": [sentence_type]
            })

            identificationDf = pd.concat([identificationDf, dataDf], columns=['Prompt', 'Input', 'Output'])
            print("w")
            print(identificationDf)