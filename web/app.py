from distutils.log import debug
from flask import Flask, jsonify, requests
from pymongo import MongoClient
from flask_restful import Resources, Api

app = Flask(__name__)
api = Api(app)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)