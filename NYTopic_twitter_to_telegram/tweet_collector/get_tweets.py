"""module to connect to Twitter API and extract tweets 
from the New York Times account into a mangodb container."""

import os
import sys
import logging
from time import sleep
from urllib3.exceptions import ReadTimeoutError

import pymongo
from tweepy import OAuthHandler, Cursor, API, Stream
from tweepy.streaming import StreamListener


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO, filename='get_tweets.log')


API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("SECRET_ACCESS_TOKEN")



def authenticate():
    """Function for handling Twitter Authentication."""
     
    auth = OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = API(auth)

    return api, auth


def authentication_attempt():
    """Try/Except pattern for authentication"""
    try:
        api, auth = authenticate()
        logging.warning("Twitter authentication successful!")
        return api, auth
    except:
        logging.warning("Failed Twitter authentication. Exiting.")
        sys.exit()


def cursor_cycle():
    """Function for reading the last 10 tweets from the NYT's Twitter timeline and sending the relevant one to the MongoDB container."""

    for status in cursor.items(10):
        text = status.full_text

        # take extended tweets into account and rule out retweets
        if "extended_tweet" in dir(status):
            text = status.extended_tweet.full_text

        if "retweeted_status" in dir(status):
            continue

        tweet = {
            "text": text,
            "username": status.user.screen_name,
            "tweet_date": status.created_at,
        }

        collection.insert_one(tweet)
        logging.warning(f"Found a tweet: inserted into MongoDB: {text}")


class MyStreamListener(StreamListener):
    """Class for handling the realitime twitter streaming of the NYT by sendind the relevant ones to the MongoDB container."""

    def __init__(self, max_tweets=100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set the instance attributes
        self.max_tweets = max_tweets
        self.counter = 0
        self.non_relevant_counter = 0

    def on_connect(self):
        logging.warning("Now listening for incoming tweets.")

    def on_status(self, status):
        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        # increase the counter
        self.counter += 1
        if status.user.screen_name != "nytimes":
            self.non_relevant_counter += 1
        else:
            try:
                tweet_text = status.extended_tweet["full_text"]
            except:
                tweet_text = status.text

            tweet = {"text": tweet_text,
                "username": status.user.screen_name,
                "tweet_date": status.created_at}

            # check if we have enough tweets collected
            if self.max_tweets == self.counter:
                # reset the counters
                self.counter = 0
                logging.warning("Maximum reached. Pausing for not going into overload...")
                logging.warning(f"Non relevant incoming tweets detected and skipped during this cycle: {self.non_relevant_counter}.")
                self.non_relevant_counter = 0
                #return False to stop the listener
                return False
            else:
                if tweet["text"][:4] == "RT @":
                    self.non_relevant_counter += 1
                else:
                    logging.warning(f'{tweet["tweet_date"]}: New relevant tweet arrived from NYT: {tweet["text"]}. Inserted into MongoDB.')
                    collection.insert_one(tweet)

    def on_error(self, status):
        if status == 420:
            logging.critical(f"Rate limit applies. Stopping the stream for a few minutes.")
            logging.warning(f"Non relevant incoming tweets detected and skipped during this cycle: {self.non_relevant_counter}.")
            self.non_relevant_counter = 0
            return False

#connect to the container that has mongo on it; create a database on mongo called "tweet_collector"
client = pymongo.MongoClient("mongodb")
db = (client.tweet_collector)  

#create a collection called "tweet_data"
collection = db.tweet_data

# initial loading of past tweets (runs for six hours)
api, auth = authentication_attempt()
cursor = Cursor(api.user_timeline, id="nytimes", tweet_mode="extended")

for cycle in range(10800):
    cursor_cycle()
    sleep(2)

# Start the live-stream after initial loading
while True:
    api, auth = authentication_attempt()
    logging.warning("Starting a streaming phase...")
    NYTStreamListener = MyStreamListener()
    try:
        my_stream = Stream(auth=auth, listener=NYTStreamListener, tweet_mode="extended")
        my_stream.filter(follow=["807095"])
    except ReadTimeoutError as e:
        logging.error(f"{e.args}. This is normal after a while. Restarting the stream...")
        continue
    sleep(60 * 5)
    logging.warning("Checking if anything relevant has been tweeted during the pause of the streaming.")
    api, auth = authentication_attempt()
    cursor = Cursor(api.user_timeline, id="nytimes", tweet_mode="extended")
    cursor_cycle()
