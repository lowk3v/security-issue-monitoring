import logging
import logging.handlers
from os import environ

class Logger:
    def __init__(self):
        environ['TZ'] = 'Asia/Ho_Chi_Minh'
        HOME = environ.get('NEWSFEED_HOME', '.') + '/'
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        access_handler = logging.handlers.RotatingFileHandler(
            HOME+"logs/access.log",
            maxBytes=1000000,
            backupCount=20)
        error_handler = logging.handlers.RotatingFileHandler(
            HOME+"logs/error.log",
            maxBytes=1000000,
            backupCount=20)

        access_handler.setFormatter(formatter)

        self.error = logging.getLogger('error')
        self.error.setLevel(logging.DEBUG)
        self.error.addHandler(error_handler)

        self.access = logging.getLogger('access')
        self.access.setLevel(logging.INFO)
        self.access.addHandler(access_handler)
