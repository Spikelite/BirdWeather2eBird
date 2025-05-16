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