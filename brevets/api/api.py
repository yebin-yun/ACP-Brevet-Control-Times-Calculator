from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from bson import json_util
import json
import db # Database operations
import os
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer \
                                  as Serializer, BadSignature, \
                                  SignatureExpired)
import time

app = Flask(__name__)
api = Api(app)

db_client = db.Mongodb(os.environ['MONGODB_HOSTNAME'])
db_client.connect()
db_client.set_db("brevetsdb")

parser = reqparse.RequestParser()
parser.add_argument('username', required=True, help="Need an username!")
parser.add_argument('password', required=True, help="Need a password!")

SECRET_KEY = ""

def csv_form(rows):
    headers = list(rows[0].keys())
    result = ",".join(headers) + "\n"
    for row in rows:
        row_value = [str(r) for r in list(row.values())]
        result += ",".join(row_value) + "\n"
    return result

def hash_password(password):
    return pwd_context.encrypt(password)

def verify_password(password, hashVal):
    return pwd_context.verify(password, hashVal)

def generate_auth_token(id, expiration=600):
   s = Serializer(SECRET_KEY, expires_in=expiration)
   # Pass index of user
   return s.dumps({'id': id})

def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None    # valid token, but expired
    except BadSignature:
        return None    # invalid token
    return "Success"

###
# Resources
###
class register(Resource):
    def post(self):
        db_client.set_collection("user")
        user_info = parser.parse_args()
        try:
            user_info['password'] = hash_password(user_info['password'])
            if len(db_client.filter_find({'username': user_info['username']})) == 0:
                user_info['id'] = db_client.generate_id()
                db_client.insert(user_info)
                return "Successfully added the user!", 201
            else:
                return abort(400, "The user already exists!")
        except Exception as e:
            return abort(400, e)


class token(Resource):
    def get(self):
        db_client.set_collection("user")
        # Get the argument username and password; default value will be ""
        username = request.args.get("username", default="")
        password = request.args.get("password", default="")
        # Get the argument secret key and set it to the global variable
        global SECRET_KEY
        SECRET_KEY = request.args.get("secretkey", default="secretkey272781239@#!")
        # Check if both username and password are passed in
        if username == "" or password == "":
            return abort(400, "Need both username and password!")
        # Get the user info
        user_info = db_client.filter_find(["id", "password"], {'username': username})
        # Check if the user is registered
        if len(user_info) == 1:
            user_info = user_info[0]
            auth = {"duration": 600}
            hashed_password = user_info["password"]
            id = user_info["id"]
            # Check if the password matches
            if verify_password(password, hashed_password):
                auth["token"] = generate_auth_token(id).decode("utf-8")
                app.logger.debug(f"token: {auth['token']}")
                return json.dumps(auth), 201
            # When the password doesn't match the one in the db
            return abort(400, "Wrong password. Try again!")
        else:
            return abort(400, "The username doesn't exist. Register first!")


class listBrevetTimes(Resource):
    def get(self, option="", dtype=""):
        db_client.set_collection("latestsubmit")
        # Get the argument top; default value will be -1
        top = int(request.args.get("top", default=-1))
        # Get the argument token; default value will be ""
        user_token = request.args.get("token", default="")
        # Get the argument secret key and set it to the global variable
        global SECRET_KEY
        SECRET_KEY = request.args.get("secretkey", default="secretkey272781239@#!")
        if not verify_auth_token(user_token):
            return abort(400, "Authentication failed!")
        else:
            if option == "All":
                fields = ["km", "open", "close"]
            elif option == "OpenOnly":
                fields = ["km", "open"]
            elif option == "CloseOnly":
                fields = ["km", "close"]
            else:
                return "The only possible options are listAll, listOpenOnly, listCloseOnly!"

            # When the positive argument k is passed, retrieve the top k rows with the specific fields in the collection
            if top > 0:
                rows = db_client.find_top_k(fields, top)
            # When the argument is not passed, retrieve all the rows with the specific fields in the collection
            elif top == -1:
                rows = db_client.filter_find(fields)
            else:
                return "Need to pass a positive number for top!"
            # Check if the collection is empty
            if len(rows) == 0:
                return "The database is empty. Please, submit the control time."
            # Check the data type
            if dtype == 'csv':
                result = csv_form(rows)
            elif dtype == 'json' or dtype == "":
                result = json.loads(json_util.dumps(rows))
            else:
                result = "The data can be listed in either csv format or json format! Try 'csv' or 'json'."
            return result

#############

# Create routes
api.add_resource(listBrevetTimes, '/list<string:option>', '/list<string:option>/<string:dtype>')
api.add_resource(register, '/register')
api.add_resource(token, '/token')


# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
