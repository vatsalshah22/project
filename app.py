from flask import Flask
from flask import render_template
from flask import jsonify

app=Flask(__name__)

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/detect")

def detect():

    return jsonify({

        "name":"Vatsal"

    })
