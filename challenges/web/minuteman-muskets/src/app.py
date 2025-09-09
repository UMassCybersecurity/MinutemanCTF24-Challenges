from flask import Flask, render_template, request
import os

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='/app/public/')

TOKEN = int(open("/app/token").read()) % 1000
FLAG = os.environ["FLAG"]

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/guess",methods=["POST"])
def guess():
    if("code" in request.json and request.json.get("code") == TOKEN):
        return {'correct':FLAG}
    return {'incorrect':'Try another number.'}
