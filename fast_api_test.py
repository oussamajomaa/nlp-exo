# Dependencies:
# pip install bert-extractive-summarizer
# pip install python-multipart // To receive uploaded files

import os
import re
import uvicorn
# from summarizer import Summarizer,TransformerSummarizer
from transformers import pipeline

from fastapi import FastAPI, Request, UploadFile, status

from fastapi.exceptions import HTTPException

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

# Enable CORS: Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Receive text 
@app.post('/')
async def summ_text(request: Request):
    # Read the request body in json format and put it in body variable
    body = await request.json()
    params = request.query_params
    
    if params == "facebook/bart-large-cnn":
        model = "facebook/bart-large-cnn"
    elif params == "google/pegasus-xsum":
        model = "google/pegasus-xsum"
    elif params == "csebuetnlp/mT5_multilingual_XLSum":
        model = "csebuetnlp/mT5_multilingual_XLSum"
    else:
        model = "facebook/bart-large-cnn"
        
        
    print(params)
    # instanciate summarize model
    summarizer = pipeline("summarization", model=model)
    summary = summarizer(body)
    # clean text
    summary = summary[0]['summary_text'].replace(u'\xa0', u' ')
    # remove spaces
    summary = re.sub("\s\s+"," ",summary)
    return summary


@app.post('/file')
async def summ_file(file: UploadFile, request: Request):
    try:
        # Define the path where the uploade file will be saved
        filepath = os.path.join('./uploads', os.path.basename(file.filename))

        # put content file in variable body
        body = file.file.read()
        
        # save uploaded file on computer in filepath
        open(filepath, 'wb').write(body)
        
        # read the saved file and put the content in variable data
        data = open (filepath,'r').read()

        params = request.query_params
    
        if params == "facebook/bart-large-cnn":
            model = "facebook/bart-large-cnn"
        elif params == "google/pegasus-xsum":
            model = "google/pegasus-xsum"
        elif params == "csebuetnlp/mT5_multilingual_XLSum":
            model = "csebuetnlp/mT5_multilingual_XLSum"
        else:
            model = "facebook/bart-large-cnn"
            
            
        print(params)
        summarizer = pipeline("summarization", model=model)
        summary = summarizer(data)
        summary = summary[0]['summary_text'].replace(u'\xa0', u' ')
        summary = re.sub("\s\s+"," ",summary)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='There was an error uploading the file')
    return summary


if __name__ == '__main__' :
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app)