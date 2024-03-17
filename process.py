import pandas as pd
import json
from prompts import revise_review, label_review
from parser_module import parse_review
from ftfy import fix_encoding

fileName1 = "C:\\Users\\rafae\\Documents\\PrepDataSet\\Data\\manualAnnotations.jsonl"
fileName2 = "C:\\Users\\rafae\\Documents\\PrepDataSet\\Data\\automatedAnnotations.jsonl"
fileName3 = "C:\\Users\\rafae\\Documents\\PrepDataSet\\Data\\test.csv"

outputFile1 = "C:\\Users\\rafae\\Documents\\PrepDataSet\\ProcessedDatasets\\identification1.csv"
outputFile2 = "C:\\Users\\rafae\\Documents\\PrepDataSet\\ProcessedDatasets\\revision1.csv"

identificationDf = pd.DataFrame(columns=['Input', 'Output'])
revisionDf = pd.DataFrame(columns=['Input', 'Output'])

# get manually annotated sentences
with open(fileName1, 'r', encoding='utf-8') as file:
    # mapping = {
    #     "positive" : 0,
    #     "neutral" : 1,
    #     "negative" : 2
    # }
    for line in file:
        data = json.loads(fix_encoding(line))
        sentences = data.get('sentences', [])
        id = data.get("id")

        for sentence in sentences:
            sentence_type = sentence.get('sentence_type', None)
            sentence = sentence.get('sentence', None)
            
            dataDf = pd.DataFrame({
                "Id" : id,
                "Input": [sentence],
                "Output": [sentence_type]
            })

            # add data to the identification dataframe
            identificationDf = pd.concat([identificationDf, dataDf], ignore_index=True)

            # print(sentence)
            # print(identificationDf)
            ########## This part needs to be fixed ##########
            # add data to the revision dataframe
            # revisionDf.append({"Prompt": revise_review(sentence), "Sentence" : sentence, "Revision" : sentence_type})
# get automated annotations
            
with open(fileName2, 'r', encoding='utf-8') as file:
    # mapping = {
    #     "Confirmed" : 2,
    #     "Missed by Model" : 2,
    #     "Maybe" : 1,
    #     "Not concerning" : 0,
    #     "positive" : 0,
    #     "Missed Maybe" : 1
    # }
    
    for line in file:
        data = json.loads(fix_encoding(line))
        sentences = data.get('sentences', [])
        text = data.get('text', None)
        entities = data.get('entities', [])
        id = data.get("id", None)

        # add data to the identification model data set
        for entity in entities:
            index1 = entity[0]
            index2 = entity[1]
            rating = entity[2]

            dataDf = pd.DataFrame({
                "Id" : id,
                "Input": [text[index1:index2]],
                "Output": [rating]
            })

            identificationDf = pd.concat([identificationDf, dataDf], ignore_index=True)

        # add data to the revision model dataset
        for sentence in sentences:
            if sentence.get('sentence_type', None) == "2" or sentence.get('sentence_type', None) == "3":
                dataDf = pd.DataFrame({
                    "Id": [id],
                    "Input": [sentence.get('sentence', None)],
                    "Output": [sentence.get('rephrased', None)]
                })

                revisionDf = pd.concat([revisionDf, dataDf], ignore_index=True)


# get toxic samlpes from premade toxic dataset
toxicCommentsDf = pd.read_csv(fileName3)

#there are a total of 159607 toxicc comments in this dataset
numberOfComments = 500
randomCommentsDf = toxicCommentsDf[['id', 'comment_text']].sample(n=numberOfComments, random_state=42)
randomCommentsDf.rename(columns={'id': 'Id'}, inplace=True)
randomCommentsDf.rename(columns={'comment_text': 'Input'}, inplace=True)

randomCommentsDf['Output'] = [2] * len(randomCommentsDf)

identificationDf = pd.concat([identificationDf, randomCommentsDf], ignore_index=True)

# get MORE samples from OTHER datasets


print(identificationDf)
print(revisionDf)




# Save the DataFrame with custom parameters
identificationDf.to_csv(outputFile1, header=True, index=False, mode='w', encoding='utf-8')
revisionDf.to_csv(outputFile2, header=True, index=False, mode='w', encoding='utf-8')
