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
import random
import string
from datetime import datetime

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
    return f"{base_name}-{random_str}-{date_formatted}.csv"

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

# Load shapes once to improve performance for repeat lookups
country_shapes = load_shapes(config.country_shape_file, 'ISO_A2')
state_shapes = load_shapes(config.state_shape_file, 'STUSPS')

# Create optimized lookup functions once to improve performance
country_lookup = get_optimized_code_lookup(country_shapes)
state_lookup = get_optimized_code_lookup(state_shapes)