"""
core_processing.py

This library provides core functions processing .csv files as a part of
BirdWeather2eBird.

It includes functions to:
- parse_timestamp(): Parse and convert the timestamps provided by BirdWeather to be compatible with eBird's timestamps
- get_location_codes(): (Work In Progress) Get the state and country location codes from Latitude & Longitude

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

from datetime import datetime

from conf import config

def parse_timestamp(ts):
    """
    Parses the input timestamp and splits it into a date and time tuple

    Args:
        ts (str): Timestamp to parse
    
    Returns:
        Tuple containing (date,time)
    """
    dt = datetime.strptime(ts[:-6], "%Y-%m-%d %H:%M:%S")
    date = dt.strftime("%m/%d/%Y")
    time = dt.strftime("%I:%M %p")
    return date, time

def get_location_codes(lat, lon):
    """
    Gets the state and country codes for the provided latitude (lat) and longitude (lon)

    TODO: Currently this function is hard coded to return hard coded global values, in the future it should be able to
    dynamically get the location information from the lat/lon

    Args:
        lat (float): Latitude
        long (float): Longitude

    Returns:
        Tuple containing (state_code,country_code), where the code will be a 2-character code or empty
    """
    state_code = config.STATE
    country_code = config.COUNTRY

    return state_code, country_code
