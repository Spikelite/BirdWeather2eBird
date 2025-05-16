import csv

from datetime import datetime

INPUT_CSV = "birdweather_export.csv"
OUTPUT_CSV = "ebird_upload.csv"

STATE = ""
COUNTRY = ""
PROTOCOL = ""
NUM_OBSERVERS = 1
DURATION = 5
ALL_OBS_REPORTED = "Y"
DISTANCE_COVERED = ""
AREA_COVERED = ""
SPECIES_COMMENTS = ""
CHECKLIST_COMMENTS = ""

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
    state_code = STATE
    country_code = COUNTRY

    return state_code, country_code

def main():
    with open(INPUT_CSV, newline="", encoding="utf-8") as infile, \
         open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as outfile:
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
                SPECIES_COMMENTS,
                row["Station"].strip(),
                row["Latitude"],
                row["Longitude"],
                date,
                time,
                state,
                country,
                PROTOCOL,
                NUM_OBSERVERS,
                DURATION,
                ALL_OBS_REPORTED,
                DISTANCE_COVERED,
                AREA_COVERED,
                CHECKLIST_COMMENTS
            ])

if __name__ == "__main__":
    main()

