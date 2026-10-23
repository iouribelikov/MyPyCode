"""
Star utilites
"""

from pandas import DataFrame
from astropy.coordinates import SkyCoord
import astropy.units as u


def match_stars(
    v_df: DataFrame, cat_df: DataFrame, columns: set = {}, tolerance: float = 3
) -> DataFrame:
    """
    Find the closest star in "cat data frame" for every star in "v data frame"
    """

    # Matching tolerance
    tolerance *= u.arcsec

    v_coords = SkyCoord(ra=v_df["RA"].values * u.deg, dec=v_df["DEC"].values * u.deg, frame="icrs")

    cat_coords = SkyCoord(
        ra=cat_df["RA"].values * u.deg, dec=cat_df["DEC"].values * u.deg, frame="icrs"
    )

    idx, separation, _ = v_coords.match_to_catalog_sky(cat_coords)
    matched = separation < tolerance

    matched_df = v_df.loc[matched].copy()
    for col in columns:
        matched_df[col] = cat_df.iloc[idx[matched]][col].values
    matched_df.reset_index(drop=True, inplace=True)
    return matched_df
