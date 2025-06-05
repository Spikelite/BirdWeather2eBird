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

def main():
    args = cli_support.input_argparse()
    logger = cli_support.start_logging(config.log_file_path, args.log_level, config.tool_name)

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
    
    unique_dates = [] # This is used to help determine if detections spanning multiple dates are included
    species_counts = {} # Stats: Dict to track count per species
    total_detections = 0 # Stats: Total count of all detections
    detection_firstlast = {
        "first_detection": None,
        "last_detection": None
    }

    with open(args.input_file, newline="", encoding="utf-8") as infile, \
        open(output_file, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile, lineterminator="\n")
        for row in reader:
            date, time = core_processing.parse_timestamp(row["Timestamp"])
            current_datetime = datetime.strptime(row["Timestamp"][:-6], "%Y-%m-%d %H:%M:%S")
            if (args.filter_to_date) and (date != args.filter_to_date):
                logger.debug('Entry outside of provided date filter found, skipping, '
                            f'date was: {date}')
                continue
            if (detection_firstlast["first_detection"] is None or
            current_datetime < detection_firstlast["first_detection"]):
                detection_firstlast["first_detection"] = current_datetime

            if (detection_firstlast["last_detection"] is None or
            current_datetime > detection_firstlast["last_detection"]):
                detection_firstlast["last_detection"] = current_datetime
            if date not in unique_dates:
                unique_dates.append(date)
            scientific_name = row["Scientific Name"].strip()
            common_name = row["Common Name"].strip()
            scientific_name_split = scientific_name.split()
            genus = scientific_name_split[0] if len(scientific_name_split) > 0 else ""
            species = scientific_name_split[1] if len(scientific_name_split) > 1 else ""
            station_details = core_processing.set_station_details(logger, args, row)

            if args.comments:
                checklist_comments = args.comments
            else:
                checklist_comments = config.checklist_comments

            # If the checklist flag has not been set, output each detection in the eBird Record Format
            if not args.checklist:
                # The order of these datapoints are strictly required by eBird's Extended Record Format
                writer.writerow([
                    common_name,                    # Common Name
                    genus,                          # Genus
                    species,                        # Species
                    "X",                            # Species Count (int if possible, X is best when a real
                                                    #  number can not be confirmed)
                    config.SPECIES_COMMENTS,        # Species Comments
                    station_details["station_name"],# Location Name
                    station_details["latitude"],    # Latitude
                    station_details["longitude"],   # Longitude
                    date,                           # Observation Date
                    time,                           # Start Time
                    station_details["state"],       # State (2-character)
                    station_details["country"],     # Country (2-character)
                    args.protocol,                  # Protocol (Stationary,Traveling,Incidental,Historical)
                    args.number_of_observers,       # Number of Observers
                    config.DURATION,                # Duration
                    config.ALL_OBS_REPORTED,        # All Observations Reported?
                    config.DISTANCE_COVERED,        # Distance Covered
                    config.AREA_COVERED,            # Area Covered
                    checklist_comments              # Checklist Comments
                ])

            total_detections += 1
            species_counts[(common_name, scientific_name)] = species_counts.get((common_name, scientific_name), 0) + 1
    if len(unique_dates) > 1:
        logger.warning(f"Multiple dates found in input: {unique_dates}")

    if args.checklist:
        # Get time blocks:
        time_blocks = core_processing.split_time_range(detection_firstlast["first_detection"], 
                                         detection_firstlast["last_detection"],
                                         core_processing.parse_time_period(args.checklist))
        # Generate a list of block names
        block_names = ["",""]
        block_latitudes = ["Latitude",""]
        block_longitudes = ["Longitude",""]
        block_dates = ["Date",""]
        block_start_times = ["Start Time",""]
        block_states = ["State",""]
        block_countries = ["Country",""]
        block_protocols = ["Protocol",""]
        block_num_obs = ["Num Observers",""]
        block_durations = ["Duration (min)",""]
        block_all_obs_reported = ["All Obs Reported (Y/N)",""]
        block_dist_traveled = ["Dist Traveled (Miles)",""]
        block_area_covered = ["Area Covered (Acres)",""]
        block_notes = ["Notes",""]
        if args.comments:
            checklist_comments = args.comments
        else:
            checklist_comments = config.checklist_comments

        checklist_duration = core_processing.get_duration(args.checklist)
        block_count = 0
        # This list will contain all of the different block's species counts, which are also lists
        species_counts_by_block = []
        # Iterate over our time blocks so that we create separate checklist entries for each block
        for block_time in time_blocks:
            with open(args.input_file, newline="", encoding="utf-8") as infile:
                reader = csv.DictReader(infile)
                block_count += 1
                # Append the station specific information to each time block entry in their respective lists
                block_names.append(f'{station_details["station_name"]}-' \
                                       f'{core_processing.format_time_block(block_time)}')
                block_latitudes.append(station_details["latitude"])
                block_longitudes.append(station_details["longitude"])
                block_dates.append(block_time[0].date().strftime("%m/%d/%Y"))
                block_start_times.append(block_time[0].time())
                block_states.append(station_details["state"])
                block_countries.append(station_details["country"])
                block_protocols.append(args.protocol)
                block_num_obs.append("1")
                block_durations.append(checklist_duration)
                block_all_obs_reported.append("Y")
                block_dist_traveled.append("")
                block_area_covered.append("")
                block_notes.append(checklist_comments)
                # Because the species count information is a bit more dynamic and is a list of lists, we build and
                # append it to its list by iterating over each row in the input CSV and filtering to the specific time
                # block.
                block_species_counts = {(common_name, scientific_name): None for (common_name, scientific_name) in
                                        species_counts}
                for row in reader:
                    current_datetime = datetime.strptime(row["Timestamp"][:-6], "%Y-%m-%d %H:%M:%S")
                    # if start <= current <= end
                    if block_time[0] <= current_datetime <= block_time[1]:
                        scientific_name = row["Scientific Name"].strip()
                        common_name = row["Common Name"].strip()
                        species_tuple = (common_name, scientific_name)
                        block_species_counts[species_tuple] = ((block_species_counts.get(species_tuple) or 0) + 1)
                species_counts_by_block.append(block_species_counts)

        # Write the final output into the eBird Checklist Format, as a .csv
        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile, lineterminator="\n")
            writer.writerow([*block_names])
            writer.writerow([*block_latitudes])
            writer.writerow([*block_longitudes])
            writer.writerow([*block_dates])
            writer.writerow([*block_start_times])
            writer.writerow([*block_states])
            writer.writerow([*block_countries])
            writer.writerow([*block_protocols])
            writer.writerow([*block_num_obs])
            writer.writerow([*block_durations])
            writer.writerow([*block_all_obs_reported])
            writer.writerow([*block_dist_traveled])
            writer.writerow([*block_area_covered])
            writer.writerow([*block_notes])
            # This unpacks our nested species lists and ensures that they are written properly in the output with their
            # common name and species name (*species_key) as the first two columns of each row, followed by the totals
            # for each time block.
            for species_key in species_counts:
                row = [block.get(species_key, 0) for block in species_counts_by_block]
                writer.writerow([*species_key, *row])

    if args.stats:
        logger.info('')
        logger.info('Processed File Stats')
        logger.info(f'Total Detections: {total_detections}')
        logger.info(f'Total Species: {len(species_counts)}')
        logger.info('')
        logger.info('Species Stats')
        for species, count in species_counts.items():
            logger.info(f'{species}: {count}')
        logger.info('')

    logger.info('BirdWeather2eBird ran Successfully!')

if __name__ == "__main__":
    main()
