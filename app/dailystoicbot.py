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

    def _get_random_daily_stoic_quote(self, retries: int = 3):
        """"""
        random_stoic_quote_url = 'https://stoic-server.herokuapp.com/random'

        for i in range(retries):
            try:
                # Make a request for a random stoic quote.
                response = requests.get(random_stoic_quote_url)
                data = response.json()

                # Retrieve the quote object from the data returned.
                quote_data = data[0]
                if any(key in quote_data for key in ('status', 'statusCode', 'message')):
                    if i == (retries - 1):
                        # On final retry, was not able to retrieve quote.
                        logger.error('Failure to retrieve quote after maximum number of retries - %s', data)
                        raise Exception('Failure to retrieve quote after maximum number of retries - %s', data)

                    # Log the failure to retrieve the quote.
                    logger.warning('An error occurred when retrieving a stoic quote from the API - %s', data)

                    # Continue to the next retry.
                    continue
                else:
                    return StoicQuote(quote_data)

            except RequestException as request_ex:
                logger.error(str(request_ex))
                raise request_ex
