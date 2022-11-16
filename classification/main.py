# NAMED ENTITY VIA HUGGINGFACE

import os
from flask import Flask, request

from flask_cors import CORS
from werkzeug.utils import secure_filename
import json


from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['POST'])
def index():
    results = []
    # Get body request as text
    text = request.get_json(force=True)
    text = text["text"]

    # Get params request
    model_name = request.args.get('model')
    results = extract_location(model_name,text)

    return json.dumps(results)


def extract_location(model_name,text):
    results = []
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    entities = nlp(text)
    print(entities)
    for ent in entities:
        if model_name == "dslim/bert-base-NER":
            if ent['entity'] == 'I-LOC' or ent['entity'] == 'B-LOC':
                results.append({"city":ent['word']})

        if model_name == "elenanereiss/bert-german-ler":
            if ent['entity'] == 'B-ST' or ent['entity'] == 'B-LD':
                results.append({"city":ent['word']})

        if model_name == "cmarkea/distilcamembert-base-ner":
            if ent['entity'] == 'I-LOC':
                ent['word'] = ent['word'].replace("▁","")
                results.append({"city":ent['word']})
        if model_name == "CAMeL-Lab/bert-base-arabic-camelbert-msa-ner":
            if ent['entity'] == 'B-LOC':
                ent['word'] = ent['word'].replace("▁","")
                results.append({"city":ent['word']})

    return results


if __name__ == '__main__':
    app.run(port=5000,debug=True)  

# from transformers import AutoTokenizer, AutoModelForTokenClassification
# from transformers import pipeline

# # # English model
# tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
# model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

# # # German model
# # tokenizer = AutoTokenizer.from_pretrained("elenanereiss/bert-german-ler")
# # model = AutoModelForTokenClassification.from_pretrained("elenanereiss/bert-german-ler")

# # French model
# # tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
# # model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")


# nlp = pipeline("ner", model=model, tokenizer=tokenizer)

# contents = open('../uploads/en.txt', 'r', encoding='utf-8-sig').read()

# results = []
# doc = nlp(contents)
# print(doc)
# for ent in doc:
#     # germain
#     # if ent['entity'] == 'B-ST' or ent['entity'] == 'B-LD':
#     #  french
#     # if ent['entity'] == 'I-LOC':
#     # english
#     if ent['entity'] == 'I-LOC' or ent['entity'] == 'B-LOC':
#         results.append(ent['word'])
# # for ent in doc:
# #     print(doc)
#     # results.append(ent)
# #     item = {
# #         'city':ent.word,
# #         'label':ent.entity
# #     }
# #     if item['label'] == 'LOC':
# #         results.append(item)
# responses = []
# for word in results:
#     word = word.replace("▁","")
#     item = {'city':word}
#     responses.append(item)

# print(responses)