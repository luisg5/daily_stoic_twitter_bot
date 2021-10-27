# Utility functions used in the application.
import logging

LOG_FILE_NAME = 'DAILY_STOIC_TWITTER_BOT'


def get_logger(logger_name):
    """"""
    # Create the logger and set it up.
    logger = logging.getLogger(logger_name)
    logger.setLevel(level=logging.INFO)

    # Create the formatter and add it to the file handler.
    formatter = logging.Formatter(
        "%(levelname)s %(asctime)s %(filename)s:%(lineno)d - %(message)s"
    )

    # Create the file handler and set it up.
    fh = logging.FileHandler("{}.log".format(LOG_FILE_NAME))
    fh.setLevel(level=logging.INFO)
    fh.setFormatter(formatter)

    # Add the file handler to the logger.
    logger.addHandler(fh)

    return logger
