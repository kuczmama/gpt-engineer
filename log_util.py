import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = 'app.log'
logging.basicConfig(filename=LOG_FILE, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def setup_logging():
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of logs

    # Create handlers (file and console)
    file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 5, backupCount=2)
    console_handler = logging.StreamHandler()

    # Set logging level for handlers
    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)