from distutils.log import debug
import json
from urllib import request
from flask import Flask, jsonify, requests
from pymongo import MongoClient
from flask_restful import Resource, Api
import bcrypt

app = Flask(__name__)
api = Api(app)

# connecting to database
client = MongoClient("localhost", 27017)
db = client.GogglesDB
users = db["Users"]


def verifyUsername(username):
    if users.find_one({"Username": username}).count_documents() > 0:
        return True
    else:
        return False

def generateDictionary(status, message):
    retJSON = {
        "status": status,
        "message": message
    }

    return jsonify(retJSON)

def verifyLogin(username, password):
    pwd = users.find_one({"Username": username})[0]["Password"]

    if bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()) == pwd:
        return generateDictionary(302, "invalid credentials")

def getTokenCount(username):
    num_count = users.find_one({"Username": username})[0]["Tokens"]
    return num_count

# User register end point
class Register(Resource):
    def post(self):

        #get posted data
        postedData = requests.get_json()

        # get username and password from posted data
        username = postedData["username"]
        password = postedData["password"]

        user_exists = verifyUsername(username)

        # if the username is taken send a fail response
        if user_exists:
            return generateDictionary(301,"username already exists. try another username or login if the account belongs to you" )
        
        # if the username is available, complete the registration

        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 10
        })

        return generateDictionary(200, "Registration successful")

# refill endpoint 
class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        # get username and admin password
        username = postedData["username"]
        admin_pw = postedData["admin_pw"]
        refill_amt = postedData["refill_amt"]

        # admin_pw
        admin_key = "3647sgshsk"

        if not admin_key == admin_pw:
            return generateDictionary(305, "Wrong admin password")

        if admin_key == admin_pw:
            return generateDictionary(200, "Tokens added")

        count = getTokenCount(username)

        users.update_one(
            {
                "Username": username
            }, 
            {
                "$set": {
                    "Tokens": refill_amt + count
                }
            })
        
api.add_resource(Register, '/register')
api.add_rosourve(Refill, '/refill')


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)