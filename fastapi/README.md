# Create an environment
### python3 -m venv name_environment

<br><br>

# Install uvicorn to start a server
### pip install uvicorn

<br><br>

# Install gunicorn
## to deploy on heroku
### pip install gunicorn

<br><br>

# Install pydantic
## who allows custom data types to be defined or you can extend validation with methods on a model decorated with the validator decorator
### pip install pydantic

<br><br>

# Install fastapi
## it is a modern, fast (high-performance), web framework for building APIs with Python 3.7+
### pip install fastapi

<br><br>

# Install sklearn
## Scikit-learn (formerly scikits.learn and also known as sklearn) is a free software machine learning library for the Python programming language
### pip instal sklearn

<br><br>

# Install pandas
## it is an open source Python package that is most widely used for data science/data analysis and machine learning tasks. It is built on top of another package named Numpy, which provides support for multi-dimensional arrays.
### pip install pandas

<br><br>

# In one command
### pip install uvicorn gunicorn pydantic fastapi pandas sklearn

<br><br>

# Run server uvicorn from terminal
### uvicorn main:app --reload

<br><br>

# Run server in script python

```
from fastapi import FastAPI

import uvicorn

app = FastAPI()

@app.get('/')
async def index():
    return {"hello":"world"}


if __name__ == '__main__' :
    uvicorn.run(app)
```
### uvicorn main:app --reload


<br><br>

# Active virtual environment:
### cd fast_api
### cd bin
### source activate

<br><br>

# Desactive virtual environment:
### cd fast_api
### cd bin
### source desactivate

<br><br>

# some error:
## 