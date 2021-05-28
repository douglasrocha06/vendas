from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app2 = Flask(__name__)
CORS(app2)

app3 = Flask(__name__)
CORS(app3)