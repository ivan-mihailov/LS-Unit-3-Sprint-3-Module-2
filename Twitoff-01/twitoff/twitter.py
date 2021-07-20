import os
import tweepy
import spacy
import en_core_web_sm
from .models import db, User, Tweet

# Authenticate user to allow use of the Twitter API
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_SECRET_KEY = os.getenv("TWITTER_SECRET_KEY")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY)
api = tweepy.API(auth)

def add_or_update_user(username):

    twitter_user = api.get_user(username)

    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id, username=username)
    db.session.add(db_user)

    tweets = twitter_user.timeline(
            count=100,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id
        )
    
    if tweets:
        db_user.newest_tweet_id = tweets[0].id
    
    nlp_model = en_core_web_sm.load() # Load SpaCy NLP model
    word2vec = nlp_model(tweets[0].text).vector # Transform latest tweet to Vector using SpaCy NLP Model
    
    for tweet in tweets:
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text, emb_tweet = word2vec)
        db_user.tweets.append(db_tweet)
        db.session.add(db_tweet)

    db.session.commit()