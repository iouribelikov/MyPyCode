"""
file: test_debug_switch_argument.py
brief:
usage: python3 test_debug_switch_argument.py
note:
author: Name, email address
"""

from taf_logger import Logger as LOG
from argparse import ArgumentParser
from yaml import load as ymlLoad
from yaml import FullLoader as ymlFullLoader
from pprint import pformat
from taf_data_handler import get_df_from_rootfile


def main(name_config_file: str, debug: bool) -> None:
    """
    Main function

    Args:
        debug (bool): Switch for debugging
    """
    if debug:
        LOG("Debug mode activated!", "DEBUG")

    LOG(name_config_file, "INFO")

    config: dict = {}
    with open(name_config_file, "r", encoding="utf-8") as yml_config_file:
        config = ymlLoad(yml_config_file, ymlFullLoader)

    input = config["input"]
    file = input["file"]
    tree = input["tree"]
    branches = input["branches"]
    df = get_df_from_rootfile(file, tree, branches)
    LOG(df.head(5), "RESULT")


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="program_name.py",
        description="Description of the program",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("-d", "--debug", default=False, action="store_true", help="debug flag")
    parser.add_argument(
        "name_config_file",
        metavar="name_config_file",
        #    default="config.yml",
        help="YAML configuration file",
    )
    args = parser.parse_args()
    main(args.name_config_file, args.debug)
