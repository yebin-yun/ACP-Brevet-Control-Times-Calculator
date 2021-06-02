from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson import json_util
import json
import db # Database operations
import os


app = Flask(__name__)
api = Api(app)

db_client = db.Mongodb(os.environ['MONGODB_HOSTNAME'])
db_client.connect()
db_client.set_db("brevetsdb")
db_client.set_collection("latestsubmit")


def csv_form(rows):
    headers = list(rows[0].keys())
    result = ",".join(headers) + "\n"
    for row in rows:
        row_value = [str(r) for r in list(row.values())]
        result += ",".join(row_value) + "\n"
    return result

###
# Resources
###

class listAll(Resource):
    def get(self, dtype=""):
        # Get the argument top; default value will be -1
        args = int(request.args.get("top", default=-1))
        fields = ["km", "open", "close"]
        # When the positive argument k is passed, retrieve the top k rows with the specific fields in the collection
        if args > 0:
            rows = db_client.find_top_k(fields, args)
        # When the argument is not passed, retrieve all the rows with the specific fields in the collection
        elif args == -1:
            rows = db_client.find_fields(fields)
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


class listOpenOnly(Resource):
    def get(self, dtype=""):
        # Get the argument top; default value will be -1
        args = int(request.args.get("top", default=-1))
        fields = ["km", "open"]
        # When the positive argument k is passed, retrieve the top k rows with the specific fields in the collection
        if args > 0:
            rows = db_client.find_top_k(fields, args)
        # When the argument is not passed, retrieve all the rows with the specific fields in the collection
        elif args == -1:
            rows = db_client.find_fields(fields)
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


class listCloseOnly(Resource):
    def get(self, dtype=""):
        # Get the argument top; default value will be -1
        args = int(request.args.get("top", default=-1))
        fields = ["km", "close"]
        # When the positive argument k is passed, retrieve the top k rows with the specific fields in the collection
        if args > 0:
            rows = db_client.find_top_k(fields, args)
        # When the argument is not passed, retrieve all the rows with the specific fields in the collection
        elif args == -1:
            rows = db_client.find_fields(fields)
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
api.add_resource(listAll, '/listAll', '/listAll/<string:dtype>')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:dtype>')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:dtype>')


# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
