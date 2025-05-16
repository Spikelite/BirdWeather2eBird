"""
BirdWeather2eBird.py

Author: Spike Graham
Copyright (c) 2025 Spike Graham
All rights reserved.

This software is provided for reference purposes only.
No license is granted to use, reproduce, modify, or distribute this code
without explicit written permission from the author.
"""

import csv

from conf import config
from lib import core_processing
from lib import cli_support

args = cli_support.input_argparse()
logger = cli_support.start_logging(config.log_file_path, config.log_level, config.tool_name)

def main():
    logger.info('Running BirdWeather2eBird')
    logger.debug(f'Input File: {args.input_file}')
    logger.debug(f'Output File: {args.output_file}')
    with open(args.input_file, newline="", encoding="utf-8") as infile, \
         open(args.output_file, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile, lineterminator="\n")
        for row in reader:
            date, time = core_processing.parse_timestamp(row["Timestamp"])
            sci = row["Scientific Name"].strip().split()
            genus = sci[0] if len(sci) > 0 else ""
            species = sci[1] if len(sci) > 1 else ""
            #state, country = core_processing.get_location_codes(row["Latitude"], row["Longitude"])
            state = args.state_code
            country = args.country_code
            # The order of these datapoints are strictly required by eBird's Extended Record Format
            writer.writerow([
                row["Common Name"].strip(), # Common Name
                genus,                      # Genus
                species,                    # Species
                "X",                        # Species Count (int if possible, X is best when a real
                                            #  number can not be confirmed)
                config.SPECIES_COMMENTS,    # Species Comments
                row["Station"].strip(),     # Location Name
                row["Latitude"],            # Latitude
                row["Longitude"],           # Longitude
                date,                       # Observation Date
                time,                       # Start Time
                state,                      # State (2-character)
                country,                    # Country (2-character)
                args.protocol,              # Protocol (Stationary,Traveling,Incidental,Historical)
                args.number_of_observers,   # Number of Observers
                config.DURATION,            # Duration
                config.ALL_OBS_REPORTED,    # All Observations Reported?
                config.DISTANCE_COVERED,    # Distance Covered
                config.AREA_COVERED,        # Area Covered
                args.comments               # Checklist Comments
            ])
    logger.info('BirdWeather2eBird ran Successfully!')

if __name__ == "__main__":
    main()
