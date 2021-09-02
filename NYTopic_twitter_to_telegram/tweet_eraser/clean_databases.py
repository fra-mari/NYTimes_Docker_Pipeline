"""Keep the database containers from growing too big by removing records older than a year from them. Runs once per day."""

import os
import logging
from time import sleep
import datetime as dt
import pymongo
from sqlalchemy import create_engine

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO, filename='clean_databases.log')

FRMT = "%Y-%m-%d %H:%M:%S"

# importing the postgres password
PW = os.getenv("POSTGRES_PASSWORD")

# connecting to the databases
client = pymongo.MongoClient("mongodb")
db = client.tweet_collector
collection = db.tweet_data

pg = create_engine(f"postgresql://postgres:{PW}@postgresdb:5432/nytimes")

def database_cleaner():
    '''Removes tweets older than a year from MongoDB and PostrgreSQL containers.'''

    #Take the date
    today = dt.datetime.strptime(dt.datetime.today().strftime(FRMT),FRMT) 
    a_year_ago = today - dt.timedelta(days=365)
    
    #Mongo
    mongo_query = { "tweet_date" : { "$lt" : a_year_ago } }
    
    logging.info(f'{len(list(collection.find()))} records currently in MongoDB.')
    gone = collection.delete_many(mongo_query)
    logging.warning(f'{gone.deleted_count} tweets older than a year deleted from MongoDB. Remaining records: {len(list(collection.find()))}.')
    
    #Postgres
    psql_query = f"""DELETE from tweets_transformed
            WHERE date < '{a_year_ago}'
            ;
    """
    count_before = pg.execute('''SELECT COUNT(*) FROM tweets_transformed;''').fetchall()[0][0]
    logging.info(f"{count_before} records currently in PostgreSQL.")
    pg.execute(psql_query)
    count_after = pg.execute('''SELECT COUNT(*) FROM tweets_transformed;''').fetchall()[0][0]
    logging.warning(f"{count_before-count_after} tweets older than a year erased from Postgres. Remaining records: {count_after}.")


logging.warning('The Database Cleaner is up and running.')
while True:
    logging.warning('A new cleaning cycle will be run in 24 hours.')
    sleep(60*60*24)
    logging.warning('Time to clean up some records from MongoDB and PostgreSQL.')
    database_cleaner()
