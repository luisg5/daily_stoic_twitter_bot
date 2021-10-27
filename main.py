# This is a sample Python script.
import os

import requests
import sqlite3

from typing import Dict, Union
from requests import RequestException
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

from app.utils import get_logger

# Load the environment variables to connect to the Twitter API.
load_dotenv()

# Note: Access protected resources. OAuth1 access tokens typically do not expire
# and may be re-used until revoked by the user or yourself.

# Get the logger to use. Note: get_logger() expects `LOGGER_NAME` env var to be set, so `load_dotenv` is called before.
# TODO: Weed out this dependency issue in future iteration.
main_logger = get_logger()


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class TwitterApiClient:
    def __init__(self):
        """"""
        consumer_key = os.getenv('CONSUMER_KEY')
        consumer_secret = os.getenv('CONSUMER_SECRET')
        access_token = os.getenv('ACCESS_TOKEN')
        token_secret = os.getenv('TOKEN_SECRET')

        self.header_oauth = OAuth1(consumer_key, consumer_secret, access_token,
                                   token_secret, signature_type='auth_header')

    def request(self):
        """"""
        pass

    def post_tweet(self, data: Union[str, Dict[str, str]]):
        """"""
        url = 'https://api.twitter.com/1.1/statuses/update.json'

        try:
            if type(data) is str:
                # Shortcut when only posting a status.
                data = {'status': data}

            response = requests.post(url, data=data, auth=self.header_oauth)
            _ = response.json()

        except RequestException as request_ex:
            main_logger.error(str(request_ex))
            raise request_ex


class StoicQuote:
    def __init__(self, quote_data: {str: str}):
        self.id = quote_data['id']
        self.quote = quote_data['body']
        self.author = quote_data['author']
        self.source = quote_data['quotesource']
        self.keywords = quote_data['keywords']
        self.document_with_weights = quote_data['document_with_weights']


class DailyStoicBot:
    def __init__(self, db_cursor: sqlite3.Cursor):
        """"""
        self.twitter_api_client = TwitterApiClient()
        self.db_cursor = db_cursor

    def start(self):
        """"""
        # TODO: Add error handling, so a quote is not saved into the database if there is an error posting it to
        #  twitter. Also, add error handling when error posting to twitter, such as retries.
        random_stoic_quote = self._get_random_daily_stoic_quote()

        twitter_status = '"{}" - {} / {}'.format(
            random_stoic_quote.quote, random_stoic_quote.author, random_stoic_quote.source)

        self.twitter_api_client.post_tweet(twitter_status)

        # Store the stoic quote id, to indicate it has already been tweeted.
        self.db_cursor.execute("INSERT INTO tweeted_stoic_quotes VALUES (?)", (random_stoic_quote.id,))

    def _get_random_daily_stoic_quote(self):
        """"""
        random_stoic_quote_url = 'https://stoic-server.herokuapp.com/random'
        try:
            response = requests.get(random_stoic_quote_url)
            data = response.json()

            if not data:
                # TODO: Log and handle this case.
                main_logger.critical('Daily Stoic Quote API returned an empty list response, no quote.')
                raise Exception('Daily Stoic Quote API returned an empty list response, no quote.')

            quote_data = data[0]
            if any(key in quote_data for key in ('status', 'statusCode', 'message')):
                print(quote_data['message'])  # Log this, it might be a failed response.
            else:
                # TODO: Save id in a personal DB. Later add code to ensure same quote is not tweeted multiple times.
                return StoicQuote(quote_data)

        except RequestException as request_ex:
            main_logger.error(str(request_ex))
            raise request_ex


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create a connection to the database that stores which stoic quotes have been tweeted.
    con = None

    try:
        # Create a connection to the database.
        con = sqlite3.connect(os.getenv('DB_NAME'))

        # Create a cursor.
        cursor = con.cursor()

        # Create the table that stores which quotes have already been tweeted.
        cursor.execute('CREATE TABLE IF NOT EXISTS tweeted_stoic_quotes (id INTEGER PRIMARY KEY)')

        # Create and start the twitter bot.
        daily_stoic_bot = DailyStoicBot(cursor)
        daily_stoic_bot.start()

        # Commit the changes.
        con.commit()

    except Exception as general_exception:
        main_logger.error(str(general_exception))

    finally:
        if con:
            con.close()

    # url = 'https://api.twitter.com/1.1/statuses/update.json'
    # data = {
    #     'status': 'Hello World! This is the Daily Stoic Bot!'
    # }
    #
    # r = requests.post(url, data=data, auth=auth)
    # print(r)
    # print(r.text)
    # print(r.json())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
