import argparse
import sys

from conf import config as config

def input_argparse():
    # Setting up argparse for CLI execution
    parser = argparse.ArgumentParser(prog=config.tool_name)
    parser.add_argument(
        "-i", 
        "--input_file",
        action="store",
        metavar="PATH",
        help="Input .csv file path",
        default=config.INPUT_CSV
    )
    parser.add_argument(
        "-o", 
        "--output_file",
        action="store",
        metavar="PATH",
        help="Output .csv file path",
        default=config.OUTPUT_CSV
    )
    parser.add_argument(
        "--state_code",
        action="store",
        metavar="XX",
        help="2-character state code, i.e. WA",
        default=config.STATE
    )
    parser.add_argument(
        "--country_code",
        action="store",
        metavar="XX",
        help="2-character country code, i.e. US",
        default=config.COUNTRY
    )
    parser.add_argument(
        "-p", 
        "--protocol",
        choices=["Stationary", "Traveling", "Incidental", "Historical"],
        help="eBird Protocol that was used for observations",
        default=config.PROTOCOL
    )
    parser.add_argument(
        "--number_of_observers",
        action="store",
        metavar="INT",
        help="Number of observers present at time of data collection",
        default=config.NUM_OBSERVERS
    )
    parser.add_argument(
        "--comments",
        action="store",
        metavar="STR",
        help="Checklist Comments to include with submissions",
        default=config.CHECKLIST_COMMENTS
    )

    return parser.parse_args()
