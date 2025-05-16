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

