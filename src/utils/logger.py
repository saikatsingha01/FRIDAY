import logging
import os


LOG_FOLDER = "logs"

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)


logging.basicConfig(

    filename=os.path.join(
        LOG_FOLDER,
        "friday.log"
    ),

    level=logging.DEBUG,

    format=
    "%(asctime)s | %(levelname)s | %(message)s",

)


def debug(message):

    logging.debug(message)



def info(message):

    logging.info(message)



def warning(message):

    logging.warning(message)



def error(message):

    logging.error(message)