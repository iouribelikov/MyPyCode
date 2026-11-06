"""
file: taf_data_handler.py
brief: Module with helper methods for analysis
author:
"""

from taf_logger import Logger as LOG

try:
    import uproot
except ModuleNotFoundError:
    print("Module 'uproot' is not installed. Please install it to run this script.")

try:
    import pandas as pd
except ModuleNotFoundError:
    print("Module 'pandas' is not installed. Please install it to run this script.")


def get_df_from_rootfile(
    name_file: str,
    name_trees: str | list[str],
    name_branches: None | list[str] | list[list[str]] = None,
) -> pd.DataFrame | list[pd.DataFrame]:
    """
    Helper function to convert a TTree inside a .root file into a pandas dataframe

    Parameters
    ------------------------------------------------
    name_file: str
        Name of input .root file

    name_trees: str | list[str]
        Name of TTree one wants to open

    name_branches: None | list[str] | list[list[str]]
        Name of TBranch objects one wants to retrieve. Select None if one wants all branches.
    """

    # retrieve only one TTree
    if not isinstance(name_trees, list):
        return uproot.open(name_file)[name_trees].arrays(name_branches, library="pd")

    if isinstance(name_branches, list):
        if not isinstance(name_branches[0], list):
            LOG("name_branches should be a list of list, as name_trees is a list!", "FATAL")

    # retrieve information
    dfs: list[pd.DataFrame] = []
    with uproot.open(name_file) as file:
        for name_tree, name_brches in zip(name_trees, name_branches):
            tree = file[name_tree]
            arrays = tree.arrays(name_brches, library="np")
            dfs.append(pd.DataFrame(arrays))
    return dfs
