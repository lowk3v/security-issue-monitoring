import logging
import logging.handlers


class Logger(object):
    logger = None

    def __init__(self):
        logger = logging.getLogger('Logger')
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler("info.log",
                                                       maxBytes=1000000,
                                                       backupCount=20)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
