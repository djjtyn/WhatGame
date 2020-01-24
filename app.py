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
def all_games():
    return render_template ("all_games.html", games=list(mongo.db.games.find()))

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
    return redirect(url_for('add_confirmation'))

@app.route('/add_confirmation')
def add_confirmation():
   return render_template('addconfirmation.html')


@app.route ('/edit_review/<game_id>')
def edit_review(game_id):
    game_review = mongo.db.games.find_one({"_id":ObjectId(game_id)})
    all_platforms =mongo.db.platforms.find()
    all_ratings = mongo.db.rating.find()
    return render_template('editreview.html',game = game_review, 
    platforms = all_platforms, ratings = all_ratings )

@app.route ('/update_review/<game_id>', methods=["POST"])
def update_review(game_id):
    games=mongo.db.games
    game_review = mongo.db.games.find_one({"_id":ObjectId(game_id)})
    games.update( {'_id': ObjectId(game_id)},
    {'game_name': request.form.get('game_name'),
     'publisher': request.form.get('publisher'),
     'release': request.form.get('release'),
     'genre': request.form.get('genre'),
     'platform': request.form.get('platform'),
     'multiplayer': request.form.get('multiplayer'),
     'rating': request.form.get('rating'),
     'description': request.form.get('description'),
     'image':request.form.get('image')
    })
    return render_template('edit_review_confirmation.html',game=game_review)

@app.route('/delete_review/<game_id>')
def delete_review(game_id):
    mongo.db.games.remove({'_id': ObjectId(game_id)})
    return redirect(url_for('all_games'))

@app.route('/show_platform_form')
def show_platform_form():
    return render_template('addplatform.html')    

@app.route('/insert_platform', methods=["POST"])
def insert_platform():
    platforms = mongo.db.platforms
    platform_doc = {'platform_name':request.form.get('platform_name')}
    platforms.insert_one(platform_doc)
    return redirect (url_for('add_review'))

@app.route ('/show_review/<game_id>')
def show_review(game_id):
    game_review = mongo.db.games.find_one({"_id":ObjectId(game_id)})
    return render_template('game_page.html',game = game_review)



if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)