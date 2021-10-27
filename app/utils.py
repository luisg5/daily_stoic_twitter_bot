# Utility functions used in the application.
import logging
import os


def get_logger():
    """"""
    # Create the logger and set it up.
    logger = logging.getLogger(os.getenv('LOGGER_NAME'))
    logger.setLevel(level=logging.INFO)

    # Create the formatter and add it to the file handler.
    formatter = logging.Formatter(
        "%(levelname)s %(asctime)s %(filename)s:%(lineno)d - %(message)s"
    )

    # Create the file handler and set it up.
    fh = logging.FileHandler("{}.log".format(os.getenv('LOGGER_NAME')))
    fh.setLevel(level=logging.INFO)
    fh.setFormatter(formatter)

    # Add the file handler to the logger.
    logger.addHandler(fh)

    return logger