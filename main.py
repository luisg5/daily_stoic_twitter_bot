# This is a sample Python script.
import os

import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()

    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    token_secret = os.getenv('TOKEN_SECRET')

    auth = OAuth1(consumer_key, consumer_secret, access_token, token_secret)

    r = requests.get(url, auth=auth)
    print(r)
    print(r.json())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
