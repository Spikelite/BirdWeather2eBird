import csv

from conf import config as config
from lib import core_processing as core

def main():
    with open(config.INPUT_CSV, newline="", encoding="utf-8") as infile, \
         open(config.OUTPUT_CSV, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile, lineterminator="\n")
        for row in reader:
            date, time = core.parse_timestamp(row["Timestamp"])
            sci = row["Scientific Name"].strip().split()
            genus = sci[0] if len(sci) > 0 else ""
            species = sci[1] if len(sci) > 1 else ""
            state, country = core.get_location_codes(row["Latitude"], row["Longitude"])
            # The order of these datapoints are strictly required by eBird's Extended Record Format
            writer.writerow([
                row["Common Name"].strip(), # Common Name
                genus,                      # Genus
                species,                    # Species
                "X",                        # Species Count (int if possible, 
                                            #                X is best when a real number can not be confirmed)
                config.SPECIES_COMMENTS,    # Species Comments
                row["Station"].strip(),     # Location Name
                row["Latitude"],            # Latitude
                row["Longitude"],           # Longitude
                date,                       # Observation Date
                time,                       # Start Time
                state,                      # State (2-character)
                country,                    # Country (2-character)
                config.PROTOCOL,            # Protocol (Stationary, Traveling, Incidental, Historical)
                config.NUM_OBSERVERS,       # Number of Observers
                config.DURATION,            # Duration
                config.ALL_OBS_REPORTED,    # All Observations Reported?
                config.DISTANCE_COVERED,    # Distance Covered
                config.AREA_COVERED,        # Area Covered
                config.CHECKLIST_COMMENTS   # Checklist Comments
            ])

if __name__ == "__main__":
    main()

