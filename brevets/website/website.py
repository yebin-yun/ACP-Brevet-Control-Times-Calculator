from flask import Flask, render_template, request, jsonify
import requests, os


###
# Globals
###

app = Flask(__name__)


###
# Pages
###

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

@app.route("/<option>")
def display(option):
    top = request.args.get("top", type=str)
    data_type = request.args.get("datatype", type=str)
    if (option == "listAll"):
        url = 'http://' + os.environ['BACKEND_ADDR'] + ':' + os.environ['BACKEND_PORT'] + '/listAll'
    elif (option == "listOpenOnly"):
        url = 'http://' + os.environ['BACKEND_ADDR'] + ':' + os.environ['BACKEND_PORT'] + '/listOpenOnly'
    else:
        url = 'http://' + os.environ['BACKEND_ADDR'] + ':' + os.environ['BACKEND_PORT'] + '/listCloseOnly'
    if data_type == "csv":
        url += '/csv'
    if int(top) > 0:
        url += '?top=' + top
    r = requests.get(url).text
    if r == '"The database is empty. Please, submit the control time."\n':
        r = "empty"
    if data_type == "csv":
        r = r.replace('\\n', '<br/>')
        r = r.replace('"', '')
    return jsonify(result=r)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
