"""SQLAlchemy models and utility functions for Twitoff Application"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create a 'user' table
class User(db.Model):
    """Twitter User Table that will correspond to tweets - SQLAlchemy syntax"""
    id = db.Column(db.Integer, primary_key = True) # id as Primary Key
    name = db.Column(db.String(50), nullable = False) # user name

    def __repr__(self):
        return "<User: {}>".format(self.name)

# Create a 'tweet' table
class Tweet(db.Model):
    """Tweet text data associated with Users Table"""
    id = db.Column(db.Integer, primary_key = True) # id as Primary Key
    text = db.Column(db.Unicode(300), nullable = False) # text of the tweet
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), \
        nullable = False)
    emb_tweet = db.column(db.pickle, nullable = False) # text of tweet after running SpaCy Model
    user = db.relationship('User', backref = db.backref('tweets', \
        lazy =  True))
    
    def __repr__(self):
        return "<Tweet: {}>".format(self.text)
