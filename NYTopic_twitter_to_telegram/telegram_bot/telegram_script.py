""""""""""""""""""""""""""""""""""""
"""Sends tweets to a telegram bot"""
""""""""""""""""""""""""""""""""""""
#built-in
import os
import logging

from time import sleep

#to pip-install
import telegram
from telegram.ext import Updater, dispatcher, CommandHandler, MessageHandler, Filters
from sqlalchemy import create_engine


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)#, filename='telegram_script.log')

###Environment variables

TOKEN = os.getenv('TOKEN2')
PW = os.getenv('POSTGRES_PASSWORD')  

###Connect to postgres

sleep(15)

pg = create_engine(f'postgresql://postgres:{PW}@postgresdb:5432/nytimes', echo=False).connect()
#pg = create_engine(f'postgresql://postgres:{PW}@localhost:5555/obama', echo=True).connect()

### Extract tweets according to keyword

def tweets_to_bot(words):
    """runs a query on the Postgres database
    #that select one tweet based on the STRING passed as argument"""

    query = f"""SELECT date, text, hashtags
        FROM tweets_transformed
        WHERE LOWER (text) ~'[ #@.‘“"-—]*{words.lower()}[ .",;:?!—”$]+'
        ORDER BY date DESC
        LIMIT 1
        ;"""

    result = pg.execute(query)
    res = list(result.fetchall())
    if len(res) != 0:
        
        t = f'''✅ The New York Times last tweeted on  “<b>{words}</b>” on {str(res[0][0])}.\n\n<i>Here's the tweet:</i>\n\n{res[0][1]}\n\n<b>Hashtags</b>: <i>{res[0][2]}</i>'''
        
        logging.warning(f'New tweet sent to bot for input keyword: "{words}".')
        
        return t
    else:
        empty = f'''TOPIC  “<b>{words}</b>”:\nI couldn't find any tweet on this topic. 🤦🏻‍♂\n\nGive another chance to my rookie programmer and think about something else to ask me!'''
        logging.warning(f'No tweet found for bot for input keyword: "{words}".')
        
        return empty

### Setting up the telegram bot

try:
    updater = Updater(token=f'{TOKEN}', use_context=True)
    logging.info('Authentication successful!')

    dispatcher = updater.dispatcher


    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello folks!👋🏻\nI'm a simple bot that selects the latest tweet of the New York Times on topics of your choice.\n\nTell me a word or a string of words! I shall see if I can find it in one of the NYT tweets...", parse_mode=telegram.ParseMode.HTML)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()

    def echo(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'{tweets_to_bot(update.message.text)}', parse_mode=telegram.ParseMode.HTML)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

except:
    logging.critical('Authentication failed.')

