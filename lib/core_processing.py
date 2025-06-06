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
import math
import random
import string
import sys
from datetime import datetime, timedelta
from typing import Tuple

import fiona
from shapely.geometry import Point, shape

from conf import config

def generate_random_string(length=6):
    """
    Generate a random alphanumeric string of the specified length.

    Args:
        length (int): Length of the string to generate. Defaults to 6.

    Returns:
        str: Random string containing lowercase letters and digits.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_filename(base_name, date_str):
    """
    Create a filename by combining a base name, a random string, and a formatted date.

    Args:
        base_name (str): Base portion of the filename (e.g., 'FileName').
        date_str (str): Date in 'MM/DD/YYYY' format.

    Returns:
        str: Formatted filename in the format 'base-random-MMDDYYYY.csv'.
    """
    date_formatted = datetime.strptime(date_str, "%m/%d/%Y").strftime("%m%d%Y")
    random_str = generate_random_string()
    return f"{base_name}-{date_formatted}-{random_str}.csv"

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

def parse_time_period(time_tuple):
    """
    Converts a tuple from the args.checklist CLI input into a timedelta.

    Accepted time units:
    - 's' for seconds
    - 'm' for minutes
    - 'h' for hours
    - 'D' for days

    Args:
        time_tuple (tuple[int, str]): A tuple with numeric value and time unit

    Returns:
        timedelta: The timedelta calculated from the input time_tuple

    Raises:
        ValueError: If the unit is invalid
    """
    amount, unit = time_tuple

    if unit == 's':
        return timedelta(seconds=amount)
    elif unit == 'm':
        return timedelta(minutes=amount)
    elif unit == 'h':
        return timedelta(hours=amount)
    elif unit == 'D':
        return timedelta(days=amount)
    else:
        raise ValueError(f"Invalid time unit: {unit}")
    
def get_duration(time_tuple):
    """
    Converts a time duration represented as a tuple into the total number of minutes,
    rounded up to the nearest minute.

    Args:
        time_tuple (tuple[int, str]): A tuple with numeric value and time unit

    Returns:
        int: The total duration in minutes, rounded up to the nearest minute.

    Raises:
        ValueError: If the unit is invalid
    """
    amount, unit = time_tuple

    if unit == 's':
        return math.ceil(amount / 60)
    elif unit == 'm':
        return math.ceil(amount)
    elif unit == 'h':
        return math.ceil(amount * 60)
    elif unit == 'D':
        return math.ceil(amount * 1440)
    else:
        raise ValueError(f"Invalid time unit: {unit}")
    
def split_time_range(start: datetime, end: datetime, interval: timedelta):
    """
    Splits a datetime range into blocks of a given interval, ensuring that
    no block spans multiple calendar days. If a block would cross midnight,
    it is truncated at 23:59:59.999999 and a new block starts at 00:00:00.

    Args:
        start (datetime): The start of the full time range
        end (datetime): The end of the full time range
        interval (timedelta): The block size

    Returns:
        List[Tuple[datetime, datetime]]: List of block (start, end) times
    """
    blocks = []
    current = start

    while current < end:
        # Tentative end of current block
        next_block_end = current + interval

        # Midnight boundary of current day
        end_of_day = datetime.combine(current.date(), datetime.max.time())

        # Ensure we don't go past end, or into next day
        block_end = min(next_block_end, end_of_day, end)

        blocks.append((current, block_end))
        current = block_end

        # If we hit the end-of-day, jump to start of next day
        if current < end and current.time() == datetime.max.time():
            current = datetime.combine((current + timedelta(days=1)).date(), datetime.min.time())

    return blocks

def format_time_block(block: Tuple[datetime, datetime]) -> str:
    """
    Formats a (start, end) datetime tuple into a string of the form:
    DDmonYY_HHMM-HHMM (e.g., 16May24_1523-1528)

    Args:
        block (Tuple[datetime, datetime]): Tuple containing start and end datetimes, on the same day

    Returns:
        str: Formatted time block string
    """
    start, end = block
    date_part = start.strftime("%d%b%y")  # e.g., 16May24
    start_time = start.strftime("%H%M")   # e.g., 1523
    end_time = end.strftime("%H%M")       # e.g., 1528
    return f"{date_part}_{start_time}-{end_time}"

def get_location_codes(lat, lon):
    """
    Gets the state and country codes for the provided latitude (lat) and longitude (lon)

    Args:
        lat (float): Latitude
        lon (float): Longitude

    Returns:
        Tuple containing (state_code, country_code), where the code will be a 2-character code or empty string if not found
    """
    country_code = country_lookup(lat, lon) or ""
    state_code = state_lookup(lat, lon) or ""
    return state_code, country_code

def load_shapes(filepath, code_field):
    """
    Loads geometric shapes and associated codes from a shapefile

    Args:
        filepath (str): Path to the shapefile (.shp)
        code_field (str): Name of the attribute field that contains the desired code (ISO country code or state code)

    Returns:
        List of tuples in the form (geometry, code), where geometry is a polygon or multipolygon and code is a string
    """
    shapes = []
    with fiona.open(filepath, 'r') as shp:
        for feature in shp:
            geom = shape(feature['geometry'])
            code = feature['properties'][code_field]
            shapes.append((geom, code))
    return shapes

def get_optimized_code_lookup(shapes):
    """
    Returns an optimized lookup function that determines the code for a given latitude and longitude,
    assuming most points will fall within the same region. Caches the first matched shape to speed up
    subsequent lookups.

    Args:
        shapes (List[Tuple[Polygon, str]]): A list of tuples containing geometries and their associated codes

    Returns:
        Callable[[float, float], Optional[str]]: A function that takes (lat, lon) and returns the matching code,
        or None if no match is found
    """
    cached_geom = None
    cached_code = None

    def find_code(lat, lon):
        nonlocal cached_geom, cached_code
        point = Point(lon, lat)

        # Check the cached geometry first
        if cached_geom and cached_geom.contains(point):
            return cached_code

        # Fall back to scanning all shapes
        for geom, code in shapes:
            if geom.contains(point):
                cached_geom = geom
                cached_code = code
                return code

        return None

    return find_code

def set_station_details(logger, args, row):
    """
    Extract and return station metadata from a single row of input, applying optional overrides.

    This function initializes a new station_details dictionary and populates it using data from the
    provided row. If `args.state_code` or `args.country_code` are provided, they will override the
    values derived from the station's latitude and longitude.

    If the same function is called again with a different station name, it logs an error and exits,
    as it is intended to handle only one station per run.

    Args:
        logger (logging.Logger): Logger for emitting error/info messages.
        args (Namespace): Parsed command-line arguments, optionally containing `state_code` and `country_code`.
        row (dict): A row of parsed CSV data with keys "Station", "Latitude", and "Longitude".

    Returns:
        dict: A dictionary with station metadata including:
              - station_name (str)
              - latitude (float)
              - longitude (float)
              - state (str)
              - country (str)
    """
    station_details = {
        "station_name": None,
        "latitude": None,
        "longitude": None,
        "state": None,
        "country": None
    }
    station_name = row["Station"].strip()

    if not station_details["station_name"]:
        station_details["station_name"] = station_name
        lat = row["Latitude"]
        lon = row["Longitude"]
        station_details["latitude"] = lat
        station_details["longitude"] = lon

        derived_state, derived_country = get_location_codes(lat, lon)

        station_details["state"] = args.state_code or derived_state
        station_details["country"] = args.country_code or derived_country

    elif station_details["station_name"] != station_name:
        logger.error("Multiple stations detected, aborting")
        logger.info("This script was only designed to work with a single station per execution")
        sys.exit()

    return station_details

# Load shapes once to improve performance for repeat lookups
country_shapes = load_shapes(config.country_shape_file, 'ISO_A2')
state_shapes = load_shapes(config.state_shape_file, 'STUSPS')

# Create optimized lookup functions once to improve performance
country_lookup = get_optimized_code_lookup(country_shapes)
state_lookup = get_optimized_code_lookup(state_shapes)