import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
from json import dumps

if path.exists("env.py"):
  import env 



app = Flask(__name__)

app.config["MONGO_DBNAME"] = "game_review"
app.config["MONGO_URI"] = os.getenv("uri")


mongo = PyMongo(app)

@app.route('/')
def all_games():
    return render_template ("all_games.html", games=list(mongo.db.games.find()))
#Code above to render home page which shows all games listed on the site
    
@app.route('/top_rated')
def top_rated():
    return render_template ("top_rated.html", games=list(mongo.db.games.find().sort("rating", -1).limit(10)))
#Code above to render top rated games page which shows the ten top most rated games on the site

@app.route('/add_review')
def add_review():
    return render_template("addreview.html", platforms = list(mongo.db.platforms.find()),
    ratings =list(mongo.db.rating.find()))
#Code above to render page showing add a review form. platforms and ratings collections included in this form

@app.route('/review_added', methods=["POST"])
def review_added():
    games = mongo.db.games
    games.insert_one(
    {'game_name': request.form.get('game_name'),
     'publisher': request.form.get('publisher'),
     'release': request.form.get('release'),
     'genre': request.form.get('genre'),
     'platform': request.form.get('platform'),
     'multiplayer': request.form.get('multiplayer'),
     'rating': int(request.form.get('rating')),
     'description': request.form.get('description'),
     'image':request.form.get('image')
    })
    return render_template('addconfirmation.html')
#Code above adds values from the form into collection keys for new documents. Rating value is passed as an int and the 
#rest are strings. After this new document is added a page showing a confirmation of the document addition is rendered.

@app.route ('/edit_review/<game_id>')
def edit_review(game_id):
    game_review = mongo.db.games.find_one({"_id":ObjectId(game_id)})
    all_platforms =mongo.db.platforms.find()
    all_ratings = mongo.db.rating.find()
    return render_template('editreview.html',game = game_review, 
    platforms = all_platforms, ratings = all_ratings )
#Code above allows the user to click on an edit button for the games which brings them to an edit form similar to the add
#review form. The only difference being that the form already has values reflecting the game pages information.

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
     'rating': int(request.form.get('rating')),
     'description': request.form.get('description'),
     'image':request.form.get('image')
    })
    return render_template('edit_review_confirmation.html',game=game_review)
#Code above updates the values in the games key values reflecting the values inserted into the edit for game form. After the
#form is sumbitted a page showing a confirmation that the edit has been sucessful is rendered

@app.route('/delete_review/<game_id>')
def delete_review(game_id):
    mongo.db.games.remove({'_id': ObjectId(game_id)})
    return redirect(url_for('all_games'))
#Code above delets documents within the games collection. After the game is deleted the home page view is called upon.
@app.route('/show_platform_form')
def show_platform_form():
    return render_template('addplatform.html')    

@app.route('/insert_platform', methods=["POST"])
def insert_platform():
    platforms = mongo.db.platforms
    platform_doc = {'platform_name':request.form.get('platform_name')}
    platforms.insert_one(platform_doc)
    return render_template('newplatform.html')
#Code above adds a platform which the user submits into the platform collection. After this addition is made a page showing
#the addition s being sucessful is rendered

@app.route ('/show_review/<game_id>')
def show_review(game_id):
    game_review = mongo.db.games.find_one({"_id":ObjectId(game_id)})
    return render_template('game_page.html',game = game_review)
#Code above allows each game review to have it's own individual URL using the document's id key

@app.route('/search', methods=["GET"])
def search():
    query=request.args.get('search')
    print(query)
    game=mongo.db.games.find_one({"game_name":query})
    return render_template("search.html", game = game)

 #   return render_template('search.html', all=all)
#Code above is an attempt at enabling a search function for the game collection database. This is still a work in progress

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)