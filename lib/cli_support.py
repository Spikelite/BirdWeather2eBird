"""
cli_support.py

This library provides utility functions for supporting CLI interactions 
with BirdWeather2eBird.

It includes functions to:
- start_logging(): Configure and start CLI based logging
- input_argparse(): Parse CLI input arguments

Example usage:
    from lib import cli_support

Author: Spike Graham
Copyright (c) 2025 Spike Graham
All rights reserved.

This software is provided for personal, non-commercial use only.  
You may view and run this software for personal educational or non-profit purposes.

You may not:
- Use this software in any commercial or enterprise context.
- Distribute modified or unmodified versions.
- Sell or include this software as part of a paid or monetized service or product.
- Use this software in any for-profit capacity.

All rights are reserved by the author.
"""

import argparse
import logging

from conf import config

def start_logging(log_path, log_level, logger_name):
    """
    Builds the logger object for logging within the API

    Args:
        log_path (str): Path to the log file for logging
        log_level (str): Logging level to use, INFO/ERROR/DEBUG

    Returns:
        object: The logger object used for logging output
    """
    logger = logging.getLogger(logger_name)
    output_format = logging.Formatter(
        '%(asctime)s [%(levelname)s]: %(message)s', "%Y-%m-%d %H:%M:%S")
    ## Setting log level
    if log_level == "INFO":
        logger.setLevel(logging.INFO)
    elif log_level == "ERROR":
        logger.setLevel(logging.ERROR)
    elif log_level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_path)
    fh.setFormatter(output_format)
    logger.addHandler(fh)
    ## Create stdout handler
    stdout = logging.StreamHandler()
    stdout.setFormatter(output_format)
    logger.addHandler(stdout)
    logger.debug('Logging Setup')
    return logger

def input_argparse():
    """
    Generates argparse for input arguments

    Args:
        None

    Returns:
        The result of parser.parse_args() after parser has been constructed
    """
    # Setting up argparse for CLI execution
    parser = argparse.ArgumentParser(prog=config.tool_name)
    parser.add_argument(
        "-i", 
        "--input_file",
        action="store",
        metavar="PATH",
        help="Input .csv file path",
        default=config.INPUT_CSV
    )
    parser.add_argument(
        "-o", 
        "--output_file",
        action="store",
        metavar="PATH",
        help="Output .csv file path",
        required=False
    )
    parser.add_argument(
        "--state_code",
        action="store",
        metavar="XX",
        help="Overrides automatic state code detection, " \
             "must be a 2-character state code, i.e. WA",
        required=False
    )
    parser.add_argument(
        "--country_code",
        action="store",
        metavar="XX",
        help="Overrides automatic country code detection, " \
             "must be a 2-character country code, i.e. US",
        required=False
    )
    parser.add_argument(
        "-p", 
        "--protocol",
        choices=["Stationary", "Traveling", "Incidental", "Historical"],
        help="eBird Protocol that was used for observations",
        default=config.PROTOCOL
    )
    parser.add_argument(
        "--number_of_observers",
        action="store",
        metavar="INT",
        help="Number of observers present at time of data collection",
        default=config.NUM_OBSERVERS
    )
    parser.add_argument(
        "--comments",
        action="store",
        metavar="STR",
        help="Checklist Comments to include with submissions",
        default=config.CHECKLIST_COMMENTS
    )

    return parser.parse_args()
