from flask import Flask, request
from flask_cors import CORS
import json
import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
 
from transformers import pipeline
from keybert import KeyBERT 
import xmltodict

@app.route('/', methods=['POST'])

    # wiki_data = requests.get("https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal").text

    # soup = BeautifulSoup(request.data, 'lxml')
    # # soup = get_xml(request.data,'lxml')
    # for p in soup.find_all('p'):
    #     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    #     summary = summarizer(p.text, max_length=250, min_length=30)

    #     # clean text
    #     summary = summary[0]['summary_text'].replace(u'\xa0', u' ')

    #     # remove spaces
    #     summary = re.sub("\s\s+", " ", summary)
    #     # rstrip() function to remove \n
    #     data.append({"p":summary})
    # return data
    # content_dict = xmltodict.parse(request.data)
    # data = []
    # # print(content_dict)
    # soup = get_xml(request.data)
    # for p in soup.find_all('title'):
    #     data.append({"p":p.text})
    # return data
    # body = json.loads(request.data)


@app.route('/', methods=['POST'])
def index():
    # body = json.loads(request.data)

    # Get body request
    body = request.get_json(force=True)

    # Get params request
    model_name = request.args.get('model')
    if model_name == "facebook/bart-large-cnn":
        from transformers import BartTokenizer, BartForConditionalGeneration
        tokenizer = BartTokenizer.from_pretrained(model_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)
    
    if model_name == "google/pegasus-xsum":
        from transformers import PegasusForConditionalGeneration, PegasusTokenizer
        tokenizer = PegasusTokenizer.from_pretrained(model_name)
        model = PegasusForConditionalGeneration.from_pretrained(model_name)

    if model_name == "csebuetnlp/mT5_multilingual_XLSum":
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    input_tokens = tokenizer.batch_encode_plus(
        [body],
        return_tensors='pt',
        max_length=1024,
        truncation=True)['input_ids']
    
    encoded_ids = model.generate(
        input_tokens,
        num_beams=4,
        length_penalty=2.0,
        max_length=100,
        min_length=50,
        no_repeat_ngram_size=3)

    if model_name == "google/pegasus-xsum":
        summary = tokenizer.batch_decode(encoded_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    else:
        summary = tokenizer.decode(encoded_ids.squeeze(), skip_special_tokens=True)



    # print(model)
    # summarizer = pipeline("summarization", model=model)
    # summary = summarizer(body, max_length=100)

    # # clean text
    # summary = summary[0]['summary_text'].replace(u'\xa0', u' ')

    # # remove spaces
    # summary = re.sub("\s\s+"," ",summary)

    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(body)
    response = {
        "summary":summary,
        "keywords":keywords
    }
    return json.dumps(response)


if __name__ == '__main__':
    app.run(port=5000,debug=True)
