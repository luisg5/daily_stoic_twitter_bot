# A class that handles retrieving random stoicism quotes.
import sqlite3

import requests

from requests import RequestException

from app.utils import get_logger
from app.twitterapiclient import TwitterApiClient

# Get the logger for this module.
logger = get_logger(__name__)


class StoicQuote:
    """"""

    def __init__(self, quote_data: {str: str}):
        self.id = quote_data['id']
        self.quote = quote_data['body']
        self.author = quote_data['author']
        self.source = quote_data['quotesource']
        self.keywords = quote_data['keywords']
        self.document_with_weights = quote_data['document_with_weights']


class DailyStoicBot:
    """"""

    def __init__(self, db_cursor: sqlite3.Cursor):
        """"""
        self.twitter_api_client = TwitterApiClient()
        self.db_cursor = db_cursor

    def start(self, retries: int = 3):
        """"""
        random_stoic_quote = self._get_random_daily_stoic_quote()

        twitter_status = '"{}" - {} / {}'.format(
            random_stoic_quote.quote, random_stoic_quote.author, random_stoic_quote.source)

        # Attempt to post the stoic tweet, with a maximum number of 3 retries.
        for i in range(retries):
            try:
                # Post the tweet using the client.
                self.twitter_api_client.post_tweet(twitter_status)

                # Store the stoic quote id, to indicate it has already been tweeted.
                self.db_cursor.execute("INSERT INTO tweeted_stoic_quotes VALUES (?)", (random_stoic_quote.id,))

                # Tweet was posted and inserted into the database successfully.
                logger.info('SUCCESS {}'.format(twitter_status))
                break

            except RequestException as request_ex:
                logger.warning('FAILURE_ATTEMPT_{} {}'.format(i, twitter_status))

    def _get_random_daily_stoic_quote(self):
        """"""
        random_stoic_quote_url = 'https://stoic-server.herokuapp.com/random'
        try:
            response = requests.get(random_stoic_quote_url)
            data = response.json()

            if not data:
                # TODO: Log and handle this case.
                logger.critical('Daily Stoic Quote API returned an empty list response, no quote.')
                raise Exception('Daily Stoic Quote API returned an empty list response, no quote.')

            quote_data = data[0]
            if any(key in quote_data for key in ('status', 'statusCode', 'message')):
                print(quote_data['message'])  # Log this, it might be a failed response.
            else:
                # TODO: Save id in a personal DB. Later add code to ensure same quote is not tweeted multiple times.
                return StoicQuote(quote_data)

        except RequestException as request_ex:
            logger.error(str(request_ex))
            raise request_ex
