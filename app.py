import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
  import env 


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "game_review"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")


mongo = PyMongo(app)

@app.route('/')
@app.route('/get_games')
def get_games():
    return render_template("games.html", games = mongo.db.games.find())
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)