from distutils.log import debug
import json
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
            retJSON = {
                "status": 301,
                "message": "username already exists. try another username or login if the account belongs to you"
            }
            return jsonify(retJSON)
        
        # if the username is available, complete the registration

        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 10
        })

        retJSON = {
            "status": 200,
            "message": "Registration successful"
        }

        return jsonify(retJSON)




if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)