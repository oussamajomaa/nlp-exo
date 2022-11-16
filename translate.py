# pip install -U deep-translator


from flask import Flask, request
from flask_cors import CORS
import json

from deep_translator import GoogleTranslator

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
 
@app.route('/translate', methods=['POST'])
def translator():
    target = request.args.get('target')
    # source = request.args.get('source')
    text = request.get_json(force=True)
    print(text)
    translated = GoogleTranslator(source="auto", target=target).translate(text)  
    print(translated)
    return json.dumps(translated)

if __name__ == '__main__':
    app.run(port=5000,debug=True)