import logging
import os
from logging.handlers import RotatingFileHandler


# Create a 'logs' directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

def get_logger(module_name):
    """Creates a preconfigured logger for a module"""
    logger = logging.getLogger(module_name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        #ensures the logs can never grow past 5mb
        file_handler = RotatingFileHandler(
        'logs/game.log', 
        maxBytes=1024 * 1024 * 5, # 5 MB
        backupCount=3             # Keeps the last 3 old log files
            )
        
        # Define the format: [Date Time] - [Level] - [Which File] - [Message]
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger