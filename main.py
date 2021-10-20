# This is a sample Python script.
import os

import requests

from requests import RequestException
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

# Note: Access protected resources. OAuth1 access tokens typically do not expire
# and may be re-used until revoked by the user or yourself.


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

    def post_tweet(self, data: {str: str}):
        """"""
        url = 'https://api.twitter.com/1.1/statuses/update.json'

        try:
            response = requests.post(url, data=data, auth=self.header_oauth)
            _ = response.json()

        except RequestException as ex:
            print(str(ex))


class StoicQuote:
    def __init__(self, quote_data: {str: str}):
        self.id = quote_data['id']
        self.quote = quote_data['body']
        self.author = quote_data['author']
        self.source = quote_data['quotesource']
        self.keywords = quote_data['keywords']
        self.document_with_weights = quote_data['document_with_weights']


class DailyStoicBot:
    def __init__(self):
        """"""
        self.twitter_api_client = TwitterApiClient()

    def start(self):
        """"""
        random_stoic_quote = self._get_random_daily_stoic_quote()
        print(random_stoic_quote.id)
        print(random_stoic_quote.quote)
        print(random_stoic_quote.author)
        print(random_stoic_quote.source)
        print(random_stoic_quote.keywords)
        print(random_stoic_quote.document_with_weights)

    def _get_random_daily_stoic_quote(self):
        """"""
        random_stoic_quote_url = 'https://stoic-server.herokuapp.com/random'
        try:
            response = requests.get(random_stoic_quote_url)
            data = response.json()

            if not data:
                # TODO: Log and handle this case.
                raise Exception('Daily Stoic Quote API returned an empty list response, no quote.')

            quote_data = data[0]
            if any(key in quote_data for key in ('status', 'statusCode', 'message')):
                print(quote_data['message'])  # Log this, it might be a failed response.
            else:
                # TODO: Save id in a personal DB. Later add code to ensure same quote is not tweeted multiple times.
                return StoicQuote(quote_data)

        except RequestException as ex:
            print(str(ex))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()

    daily_stoic_bot = DailyStoicBot()
    daily_stoic_bot.start()

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
