# A client to interact with the Twitter API.
import os

import requests

from typing import Dict, Union

from requests_oauthlib import OAuth1
from requests import RequestException

from app.utils import get_logger

# Grab a logger to use.
logger = get_logger(__name__)


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
            logger.error(str(request_ex))
            raise request_ex
