from summarizer import Summarizer
from flask import Flask, request
import os
import json
from flask_cors import CORS
from werkzeug.utils import secure_filename


app = Flask(__name__)
cors = CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
app.config['UPLOAD_PATH'] = 'uploads'
model = Summarizer()

@app.route('/', methods=['POST'])
# @cross_origin()
def resume () :
    # text = request.stream.read()
    # text = json.loads(request.data)
    text = request.get_json(force=True)

    # text = request.get_json()
    # print(text)
    res = model(text['text'],min_length=60)
    return (res)


@app.route('/file', methods=['POST'])
def resumeFile () :
    baseUrl = os.path.dirname(os.path.abspath(__file__))
    WORDS = []
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
   
    with open (baseUrl+"/uploads/"+filename,'r') as file:
        data = file.read().replace('\n','')

    data = data.replace('\ufeff','')
    # print(data)
    res = model(data,min_length=60)
    return json.dumps(res)
    


if __name__ == '__main__':
    app.run(debug=True)

