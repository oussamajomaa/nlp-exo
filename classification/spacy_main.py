# NAMED ENTITY VIA HUGGINGFACE

import os
from flask import Flask, request

from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['POST'])
def from_text():
    results = []
    # Get body request as text
    text = request.get_json(force=True)
    text = text["text"]

    # Get params request
    model_name = request.args.get('model')

    results = extract_location_from_text(model_name,text)

    return results


@app.route('/file', methods=['POST'])
def from_file():
    results = []
    model_name = request.args.get('model')
    extension = request.args.get('extension')
    file = request.files['file']
    filename = secure_filename(file.filename)

    # Save file il uploads folder
    file.save(os.path.join('uploads', filename))
    filepath = os.path.join('./uploads', os.path.basename(filename))
    
    if extension == 'txt':
        content = open(filepath, 'r', encoding='utf-8-sig').read()
        results = extract_location_from_text(model_name,content)

    if extension == 'xml':
        file = open (filepath,'r', encoding='utf-8-sig').read()
        soup = BeautifulSoup(file, 'xml')
        content = ""
        for tag in soup.find_all('p'):
            content += tag.text
        
        results = extract_location_from_text(model_name,content)

        
    # Remove file from uploads folder
    os.remove(filepath)
    
    return results



def extract_location_from_text(model_name,text):
    results = []
    if model_name == "fr_core_news_md":
        import fr_core_news_md
        nlp = fr_core_news_md.load()
        entities = nlp(text)
        for ent in entities.ents:
            if ent.label_ == "LOC":
                results.append({"city":ent.text})

    if model_name == "en_core_web_md":
        import en_core_web_md
        nlp = en_core_web_md.load()
        entities = nlp(text)
        for ent in entities.ents:
            if ent.label_ == "GPE":
                results.append({"city":ent.text})
    
    if model_name == "de_core_news_md":
        import de_core_news_md
        nlp = de_core_news_md.load()
        entities = nlp(text)
        for ent in entities.ents:
            if ent.label_ == "LOC":
                results.append({"city":ent.text})

    return results


if __name__ == '__main__':
    app.run(port=5000,debug=True)  

