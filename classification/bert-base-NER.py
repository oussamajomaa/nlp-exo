from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
# import re

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)
sentiment_pipeline = pipeline("sentiment-analysis")

contents = open('../uploads/fr.txt', 'r', encoding='utf-8-sig').read()

results = []
doc = nlp(contents)
for ent in doc:
    item = {
        'city':ent['word'],
        'label':ent['entity']
    }
    if item['label'] == 'B-LOC':
        results.append(item)

print(results)
# contents = contents.replace(',', '.').replace('?', '.')
# sentences = contents.split('.')

# # print(contents)
# for sentence in sentences:
#     result = nlp(sentence)
#     # print(result)
#     for item in result:
#         if item['entity'] == "B-LOC":
#             print(sentiment_pipeline(sentence))
#             print(item['word'])
#             # print(result)
