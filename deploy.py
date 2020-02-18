from flask import Flask, request
import requests
import flask
from flask_cors import CORS
import numpy as np
import math
import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
#    with open('requirements.txt') as f:
##        first_line = f.readline()
    
    head = str(request.headers)
    resp = flask.make_response(parser(head))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return head
    #return requests.get("https://stormy-earth-91493.herokuapp.com/",headers={"data":head}).text
    

def parser(string):
    return string[string.find("***")+3:string.find("****")]