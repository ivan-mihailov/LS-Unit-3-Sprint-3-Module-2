import os
from flask import Flask, render_template, request
from .models import db, User, Tweet

def create_app():
    """Create and configure an instance of the Flask appication."""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    
    #Create tables
    with app.app_context():
        db.create_all()

    @app.route('/', methods=["GET", "POST"])
    def home():
        name = request.form.get("name")
        if name:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()

        users = User.query.all()

        tweet = request.form.get("tweet")
        user_id = request.form.get("user_id")
        
        if tweet:
            # tweet = Tweet(text=tweet)
            # db.session.add(tweet)
            # db.session.commit()

            tweet = Tweet(text=tweet, user_id=user_id)
            # user.tweets.append(tweet)
            db.session.add(tweet)
            db.session.commit()

        tweets = Tweet.query.all()
        return render_template("home.html", title='home', users = users, tweets = tweets)
    
    return app
