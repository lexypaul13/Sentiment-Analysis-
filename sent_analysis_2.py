import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import tweepy
import nltk
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# This function allows the users to write the search items and the number of tweets he wants to explore
# this function returns nothing and draw a pie on the screen


def tweets_retrieval():
    # term used to retrieve tweets
    searchterm = input("Enter keyword to search about: ")
    # number of tweets you want to retrieve for analysis
    nb_tweets = int(input("Enter the number of tweets to analyse: "))

    # keys, token
    api_key = ""
    api_secret_key = ""
    access_token = ""
    access_token_secret = ""

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # tweets
    tweets = tweepy.Cursor(api.search, q=searchterm).items(nb_tweets)

    # analysis
    analyzer = SentimentIntensityAnalyzer()
    positive = 0
    negative = 0
    neutral = 0
    # count the number of pos, neg, neut text over the tweets
    for tweet in tweets:
        # retrieve compound for a given tweet
        compound = analyzer.polarity_scores(tweet.text)['compound']
        # apply the rules
        if compound >= 0.5:
            positive += 1
        elif 0.5 > compound > -0.5:
            neutral += 1
        elif compound <= -0.5:
            negative += 1

    positive = 100 * (positive / nb_tweets)
    negative = 100 * (negative / nb_tweets)
    neutral = 100 * (neutral / nb_tweets)

    # pie
    labels = ['Positive ' + str(round(positive, 2)) + '%',
              'Neutral ' + str(round(neutral, 2)) + '%',
              'Negative ' + str(round(negative, 2)) + '%']
    sizes = [positive, neutral, negative]
    colors = ['green', 'yellow', 'red']
    patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title("Sentiment analysis on " + searchterm + " over " + str(nb_tweets) + " tweets")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


# Bulk function,
# run and input the search item and the number of tweets you want to analyse
tweets_retrieval()
