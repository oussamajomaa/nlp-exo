from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# model_name = "dslim/bert-base-NER"
model_name = "Jean-Baptiste/camembert-ner"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)
nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

@app.route('/', methods=['POST'])
def extract_named_entities():
    article = request.get_json(force=True)

    
    named_entities = nlp(article['content'])
    locations = []
    for named_entity in named_entities:
        if named_entity['entity_group'] == 'LOC':
            locations.append(named_entity['word'])
    return locations

# example = """
# Palmyra, a rich and sometimes powerful native Aramaic-speaking kingdom arose in northern Syria in the 2nd century; the Palmyrene established a trade network that made the city one of the richest in the Roman empire. Eventually, in the late 3rd century AD, the Palmyrene king Odaenathus defeated the Persian emperor Shapur I and controlled the entirety of the Roman East while his successor and widow Zenobia established the Palmyrene Empire, which briefly conquered Egypt, Syria, Palestine, much of Asia Minor, Judah and Lebanon, before being finally brought under Roman control in 273 AD.
# """

# named_entities = nlp(example)
# locations = []
# for named_entity in named_entities:
#     if named_entity['entity'] == 'B-LOC':
#         locations.append(named_entity['word'])
#         # print(named_entity['word'])
# print(locations)


if __name__ == '__main__':
    app.run(port=5000,debug=True)