"""
file: script.py
brief: Simple script to show how to define dosctrings
usage: python3 script.py
note:
author:
"""

import module

# import pandas as pd
# TODO: Start using Pandas !

from taf_logger import Logger as LOG


def main(debug: bool = False) -> None:
    """
    _summary_

    Args:
        debug (bool, optional): _description_. Defaults to False.
    """
    if debug:
        LOG("Debug activated!", "DEBUG")

    print("In script.py, __name__: ", __name__)

    mysum(1, 2)
    module.func()


def mysum(x: float | int, y: float | int) -> float:
    """
    Helper function

    Args:
        x (float): _description_
        y (float): _description_

    Returns:
        float: _description_
    """

    return x + y


if __name__ == "__main__":
    DEBUG: bool = True
    main(DEBUG)
