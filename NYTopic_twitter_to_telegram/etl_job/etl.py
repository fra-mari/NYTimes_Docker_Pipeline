"""etl file to extract data from mangodb container, 
extract topic based hashtags from each tweet,
and send the new records to a postgres-container."""

import os
import random
import re
import logging
from time import sleep
import pymongo
import spacy
from sqlalchemy import create_engine
from sqlalchemy.sql import text

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO, filename='etl.log')

# importing the postgres password
PW = os.getenv("POSTGRES_PASSWORD")
# Loading the SpaCy model for English
nlp = spacy.load("en_core_web_sm")


# EXTRACT from mongodb (E)
def read_tweet_from_mongo():
    tweets = list(collection.find())
    if tweets:
        t = random.choice(tweets)

        logging.warning(f"Random tweet extracted from MongoDB: {t['text']}")
        return t

# TRANSFORM (T)
def add_hashtags(tweet):
    """Extract topic labels from the Tweet text and adds them to the dictionary as hashtags."""

    if tweet:
        no_url_text = re.sub(r"https://[a-zA-Z0-9./]+", "", tweet["text"]).strip()
        doc = nlp(no_url_text)
        LABELS = [
            "PERSON",
            "NORP",
            "FAC",
            "ORG",
            "GPE",
            "LOC",
            "PRODUCT",
            "EVENT",
            "WORK_OF_ART",
            "LAW"]

        hashtags = []
        for ent in doc.ents:
            if ent.label_ in LABELS:
                ent_text_regex = re.sub(r"[^\w\s]", "", ent.text)
                ent_elements = [el.lower() for el in ent_text_regex.split()]
                hashtag = f'#{"".join(ent_elements)}'
                hashtags.append(hashtag)

        hashtags = " ".join(hashtags)
        if hashtags:
            tweet["hashtags"] = hashtags
        else:
            tweet["hashtags"] = "No hashtag available for this tweet."

        return tweet


# LOAD (L)
def write_tweet_to_posgres(tweet):
    pg.execute(
        text("INSERT INTO tweets_transformed VALUES (:x,:y,:z);"),
        x=tweet["text"],
        y=str(tweet["tweet_date"]),
        z=tweet["hashtags"])  
    logging.warning("Tweet written to postgres")


if __name__ == "__main__":

    # provide the mongo-container and the postgres container with the time to run before the rest starts
    sleep(10)

    #connect to the mongodb container
    client = pymongo.MongoClient("mongodb")
    #specify the database where tweets are
    db = client.tweet_collector
    #Select the collection of documents
    collection = db.tweet_data

    #connect to the postgres container
    pg = create_engine(f"postgresql://postgres:{PW}@postgresdb:5432/nytimes")

    pg.execute(
        """
        CREATE TABLE IF NOT EXISTS tweets_transformed (
        text VARCHAR(500),
        date TIMESTAMP,
        hashtags VARCHAR(500)
        );
    """)

    sleep(10)
    logging.warning("The ETL container goes LIVE!")

    control = []
    while True:
        tweet = add_hashtags(read_tweet_from_mongo())
        if tweet:
            if tweet not in control:
                write_tweet_to_posgres(tweet)
                control.append(tweet)
                sleep(1)
            else:
                logging.warning("Tweet already in postgres: skipping.")
                sleep(1)
                continue
        else:
            logging.warning(
                "No tweet found in MongoDB. Waiting for records to write in Postgres."
            )
            sleep(60 * 30)
            continue
