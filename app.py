import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
  import env 


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "game_review"
app.config["MONGO_URI"] = os.getenv("uri")


mongo = PyMongo(app)

@app.route('/')
@app.route('/view_games')
def view_games():
    return render_template("games.html", games = list(mongo.db.games.find()))

@app.route('/add_review')
def add_review():
    return render_template("addreview.html", platforms = list(mongo.db.platforms.find()),
    ratings =list(mongo.db.rating.find()))

@app.route('/review_added', methods=["POST"])
def review_added():
    games = mongo.db.games
    games.insert_one(request.form.to_dict())
    return redirect(url_for('view_games'))

@app.route ('/edit_review/<game_id>')
def edit_review(game_id):
    game_review = mongo.db.games.find_one({"_id":ObjectId(game_id)})
    all_platforms = mongo.db.platforms.find()
    return render_template('editreview.html',review = game_review, platform = all_platforms )
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)