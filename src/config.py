import argparse
import configparser
import logging
import sys


def configure_logging():
    """
    Configure logging settings for the application.
    Logs are written both to a file and to the console.
    """
    # Initialize logger and set its logging level
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a file handler to write logs to a file
    file_handler = logging.FileHandler('./log/ATTool.log', mode='a', encoding="utf8")
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler to display logs on the console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Define the format for log messages
    formatter = logging.Formatter('[%(asctime)s - %(levelname)s] : %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def read_config_args():
    """
    Read configuration parameters from the 'setting.ini' file.

    Returns:
        tuple: A tuple containing input path, start time, end time, and output path.
    """
    config = configparser.ConfigParser()
    config.read('./setting.ini', encoding="utf8")

    # Extract settings from the configuration file
    settings = config['SETTINGS']
    return settings['input'], settings['start'], settings['end'], settings['output']
