import csv

from datetime import datetime

from conf import config as config

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

def main():
    with open(config.INPUT_CSV, newline="", encoding="utf-8") as infile, \
         open(config.OUTPUT_CSV, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile, lineterminator="\n")
        for row in reader:
            date, time = parse_timestamp(row["Timestamp"])
            sci = row["Scientific Name"].strip().split()
            genus = sci[0] if len(sci) > 0 else ""
            species = sci[1] if len(sci) > 1 else ""
            state, country = get_location_codes(row["Latitude"], row["Longitude"])
            writer.writerow([
                row["Common Name"].strip(),
                genus,
                species,
                1,
                config.SPECIES_COMMENTS,
                row["Station"].strip(),
                row["Latitude"],
                row["Longitude"],
                date,
                time,
                state,
                country,
                config.PROTOCOL,
                config.NUM_OBSERVERS,
                config.DURATION,
                config.ALL_OBS_REPORTED,
                config.DISTANCE_COVERED,
                config.AREA_COVERED,
                config.CHECKLIST_COMMENTS
            ])

if __name__ == "__main__":
    main()

