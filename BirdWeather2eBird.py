"""
BirdWeather2eBird.py

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
import csv
import os
from datetime import datetime

from conf import config
from lib import core_processing
from lib import cli_support

args = cli_support.input_argparse()
logger = cli_support.start_logging(config.log_file_path, config.log_level, config.tool_name)

def main():
    logger.info('Running BirdWeather2eBird')
    logger.debug(f'Input File: {args.input_file}')
    logger.debug(f'Output File: {args.output_file}')

    output_file = None
    file_date = None
    if args.filter_to_date:
        file_date = args.filter_to_date
    else:
        #TODO: Ideally we would pull the date from the file itself, however this is more complicated
        # to efficiently do and will be accomplished in a future revision.
        file_date = datetime.today().strftime("%m/%d/%Y")
    if args.output_file:
        output_file = args.output_file
    else:
        output_file = os.path.join(config.output_path,
                                   core_processing.generate_filename("BirdWeather2eBird", file_date))

    with open(args.input_file, newline="", encoding="utf-8") as infile, \
         open(output_file, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile, lineterminator="\n")
        # This is used to help determine if detections spanning multiple dates are included
        unique_dates = []
        station_list = []
        for row in reader:
            date, time = core_processing.parse_timestamp(row["Timestamp"])
            if (args.filter_to_date) and (date != args.filter_to_date):
                logger.debug('Entry outside of provided date filter found, skipping, '
                             f'date was: {date}')
                continue
            if date not in unique_dates:
                unique_dates.append(date)
            sci = row["Scientific Name"].strip().split()
            genus = sci[0] if len(sci) > 0 else ""
            species = sci[1] if len(sci) > 1 else ""
            station_name = row["Station"].strip()
            if (args.country_code and args.state_code):
                state = args.state_code
                country = args.country_code
            elif args.country_code:
                state, country = core_processing.get_location_codes(row["Latitude"],
                                                                    row["Longitude"])
                country = args.country_code
            elif args.state_code:
                state, country = core_processing.get_location_codes(row["Latitude"],
                                                                    row["Longitude"])
                state = args.state_code
            else:
                state, country = core_processing.get_location_codes(row["Latitude"],
                                                                    row["Longitude"])
            if args.comments:
                checklist_comments = args.comments
            else:
                checklist_comments = config.checklist_comments

            # The order of these datapoints are strictly required by eBird's Extended Record Format
            writer.writerow([
                row["Common Name"].strip(), # Common Name
                genus,                      # Genus
                species,                    # Species
                "X",                        # Species Count (int if possible, X is best when a real
                                            #  number can not be confirmed)
                config.SPECIES_COMMENTS,    # Species Comments
                station_name,               # Location Name
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
                checklist_comments          # Checklist Comments
            ])
    if len(unique_dates) > 1:
        logger.warning(f"Multiple dates found in input: {unique_dates}")
    logger.info('BirdWeather2eBird ran Successfully!')

if __name__ == "__main__":
    main()
