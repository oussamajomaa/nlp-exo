import os
from flask import Flask, request

from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
import re
from bs4 import BeautifulSoup

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
 
from transformers import pipeline
from keybert import KeyBERT 


 
@app.route('/', methods=['POST'])
def index():
    # body = json.loads(request.data)

    # Get body request
    body = request.get_json(force=True)

    # Get params request
    model_name = request.args.get('model')
    max_length = request.args.get('max_length')
    body = body.replace(u'\xa0', u' ')
    response = summary_text(body,model_name,max_length)
    return json.dumps(response)

    


@app.route('/file', methods=['POST'])
def process():
    # baseUrl = os.path.dirname(os.path.abspath(__file__))
    model_name = request.args.get('model')
    file = request.files['file']
    extension = request.args.get('extension')
    max_length = request.args.get('max_length')
    filename = secure_filename(file.filename)
    file.save(os.path.join('folder', filename))

    filepath = os.path.join('./folder', os.path.basename(filename))
    if extension == "xml":
        file = open (filepath,'r').read()
        data = {}
        data = extract_from_xml(file)

        # summary
        summaries = []
        for k, v in data.items():
            if len(v) > 0:
                obj= {
                    "title" : k,
                    "summary" : summary_text(v,model_name,max_length)
                }
                summaries.append(obj)
        # fin summary
        
        soup = BeautifulSoup(file, 'lxml')
        keyWord = soup.find("kwd-group", {"id": "kwd-group-1"})
        res = keyWord.find_all('kwd')
        kw = []
        for k in res:
            kw.append(k.text)

        print(res)
        
        response = {
            "data":summaries,
            "kw":kw
        }
        # print(data)
        return response
    
    if extension == "txt":
        f = open(filepath, "r")

        contents = f.readlines()
        # convert array to string text
        contents = " ".join(contents)
        response = summary_text(contents,model_name,max_length)
        # summarizer = pipeline("summarization", model=model)
        # summary = summarizer(contents)
        print(response)
        return json.dumps(response)




def extract_from_xml(filename):
    data = {}
    soup = BeautifulSoup(filename, 'lxml')
    abstract, intro, method, result, concl = ('' for i in range(5))
    for tag in soup.find_all('title'):
        if tag.text.strip() == 'Abstract':
            for p in tag.parent.find_all('p'):
                abstract += p.text
            data['Abstract'] = abstract.strip()
        elif 'Introduction' in tag.text.strip():
            for p in tag.parent.find_all('p'):
                intro += p.text
            data['Introduction'] = intro.strip()
        elif 'method' in tag.text.lower().strip() and method == '':
            for p in tag.parent.find_all('p'):
                method += p.text
            data['Methods'] = method.strip()
        elif 'result' in tag.text.lower().strip() and result == '':
            for p in tag.parent.find_all('p'):
                result += p.text
            data['Results'] = result.strip()
        elif ('conclusion' in tag.text.lower().strip() or 'discussion' in tag.text.lower().strip()) and concl == '':
            for p in tag.parent.find_all('p'):
                concl += p.text
            data['Conclusion'] = concl.strip()

    return data


def summary_text(body,model_name,max_length):
    if model_name == "facebook/bart-large-cnn":
        from transformers import BartTokenizer, BartForConditionalGeneration
        tokenizer = BartTokenizer.from_pretrained(model_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)
    
    if model_name == "tuner007/pegasus_summarizer":
        from transformers import PegasusForConditionalGeneration, PegasusTokenizer
        tokenizer = PegasusTokenizer.from_pretrained(model_name)
        model = PegasusForConditionalGeneration.from_pretrained(model_name)

    if model_name == "t5-large":
        from transformers import AutoTokenizer, AutoModelWithLMHead
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelWithLMHead.from_pretrained(model_name)

    if (model_name == "facebook/bart-large-cnn" or model_name == "t5-large"):
        input_tokens = tokenizer(
            [body],
            return_tensors='pt',
            max_length=1024,
            truncation=True)['input_ids']
        
        encoded_ids = model.generate(
            input_tokens,
            num_beams=4,
            length_penalty=2.0,
            max_length=int(max_length),
            min_length=round(int(max_length)/2),
            no_repeat_ngram_size=3)

        summary = tokenizer.decode(encoded_ids.squeeze(), skip_special_tokens=True)


    if model_name == "tuner007/pegasus_summarizer":
        input_tokens = tokenizer(
            body,
            return_tensors='pt',
            max_length=1024,
            truncation=True)

        encoded_ids = model.generate(**input_tokens,
            num_beams=4,
            length_penalty=2.0,
            max_length=int(max_length),
            min_length=round(int(max_length)/2),
            no_repeat_ngram_size=3)
        summary = tokenizer.decode(encoded_ids[0].squeeze(), skip_special_tokens=True)

    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(body)
    response = {
        "summary":summary,
        "keywords":keywords
    }
    return response


if __name__ == '__main__':
    app.run(port=5000,debug=True)
    # app.run('0.0.0.0', debug=True, ssl_context=('cert.pem','key.pem'))