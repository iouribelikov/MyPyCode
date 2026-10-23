"""
file: test_snippet.py
brief:
usage: python3 test_snippet.py
note:
author: Name, email address
"""

from taf_logger import Logger as LOG


def main(debug: bool) -> None:
    """
    Main function

    Args:
        debug (bool): Switch for debugging
    """
    if debug:
        LOG("Debug mode activated!", "DEBUG")


if __name__ == "__main__":
    DEBUG: bool = True
    main(DEBUG)
