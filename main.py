# This is a sample Python script.
import os

import sqlite3

from dotenv import load_dotenv

from app.utils import get_logger

from app.dailystoicbot import DailyStoicBot

# Load the environment variables to connect to the Twitter API.

# TODO: Note that DailyStoicBot is read into memory before the environment variables, so the logger file handler
#  name is not set. Fix this order.
load_dotenv()

# Note: Access protected resources. OAuth1 access tokens typically do not expire
# and may be re-used until revoked by the user or yourself.

# Get the logger to use. Note: get_logger() expects `LOGGER_NAME` env var to be set, so `load_dotenv` is called before.
# TODO: Weed out this dependency issue in future iteration.
main_logger = get_logger(__name__)


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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
