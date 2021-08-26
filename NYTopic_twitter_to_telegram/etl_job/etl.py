"""etl file to extract data from mangodb container, 
do some transformations,
and send everything to a postgres-container."""

# built-in ones
import os
import random
import re
import logging
from time import sleep

# to install
import pymongo
import spacy
from sqlalchemy import create_engine
from sqlalchemy.sql import text  

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# importing the postgres password
PW = os.getenv('POSTGRES_PASSWORD') 

#Loading the SpaCy model for English
nlp = spacy.load("en_core_web_sm")

# EXTRACT from mongodb (E)
def read_tweet_from_mongo():
    # tweet_collection is the "basket" in which our tweets are
    tweets = list(collection.find())
    if tweets:
        t = random.choice(tweets)
        
        logging.warning(f"Random tweet: {t['text']}")
        return t

# TRANSFORM (T)
def add_hashtags(tweet):
    """Extracts topic labels from the Tweet text and adds them to the dictionary as hashtags"""
    
    no_url_text = re.sub(r'https://[a-zA-Z0-9./]+', "", tweet['text']).strip()
    doc = nlp(no_url_text)
    LABELS = ['PERSON','NORP','FAC','ORG','GPE','LOC','PRODUCT','EVENT','WORK_OF_ART','LAW']

    hashtags = []
    for ent in doc.ents:
        if ent.label_ in LABELS:
            ent_text_regex = re.sub(r"[^\w\s]", '', ent.text)
            ent_elements = [el.lower() for el in ent_text_regex.split()]
            hashtag = f'#{"".join(ent_elements)}'
            hashtags.append(hashtag)

    hashtags = ' '.join(hashtags)
    if hashtags:
        tweet['hashtags'] = hashtags
    else: tweet['hashtags'] = 'No hashtag available for this tweet.'
    
    return tweet

# LOAD (L)
def write_tweet_to_posgres(tweet):
    pg.execute(text("INSERT INTO tweets_transformed VALUES (:x,:y,:z);"),
               x=tweet['text'],y=tweet['tweet_date'],z=tweet['hashtags'])  # parametrized query for preventing injection
    logging.warning('Tweet written to postgres')


if __name__ == '__main__':

    # provides the mongo-container and the postgres container with the time to run before the rest starts
    sleep(10)

    # # we connect to the container that has mongo on it. The syntax goes: kind_db://container_name:port_number/
    client = pymongo.MongoClient("mongodb")
    # specifying the database where our tweets are
    db = client.tweet_collector
    # Select the collection of documents you want to use withing the MongoDB database
    collection = db.tweet_data

    # we connect to postgres container    
    # postgresql://user:password@host(the service name, NOT the container name):port/database_name
    pg = create_engine(
        f'postgresql://postgres:{PW}@postgresdb:5432/nytimes')

    pg.execute('''
        CREATE TABLE IF NOT EXISTS tweets_transformed (
        text VARCHAR(500),
        date TIMESTAMP,
        hashtags VARCHAR(500)
    );
    ''')  

    sleep(10)
    logging.warning('The ETL container goes LIVE!')

    control = []
    while True:
        tweet = add_hashtags(read_tweet_from_mongo())
        if tweet:
            if tweet not in control:
                write_tweet_to_posgres(tweet)
                control.append(tweet)
                sleep(1)
            else:
                logging.warning('Tweet already in postgres: skipping.')
                sleep(1)
                continue        
        else:
            logging.warning('No tweet found in MongoDB. Waiting for something to write in Postgres.')
            sleep(60*30)
            continue
