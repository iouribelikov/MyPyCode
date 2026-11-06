import uproot
import pandas as pd
from taf_data_handler import get_df_from_rootfile
from taf_logger import Logger as LOG

df = get_df_from_rootfile("data.root", "tree", None)
LOG(df.head(5), "RESULT")
