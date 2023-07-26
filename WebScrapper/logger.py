import logging
from logging.handlers import RotatingFileHandler
import os

#get or create logger
def initialize_logger() -> logging:

    logger = logging.getLogger('web_scrapping_logger')
    # if it is a new logger, add handler
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        # create rotating file handler and set level to debug
        handler = RotatingFileHandler(os.path.dirname(__file__) +'\\logs\\scrapping_log.log', maxBytes=6000, backupCount=10)
        handler.setLevel(logging.DEBUG)
        #set the format and add it
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add rotating handler to logger
        logger.addHandler(handler)

    return logger

