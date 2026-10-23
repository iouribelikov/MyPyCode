"""
This script converts the CD matrix to CDELT and CROTA used by xephem
"""

from astropy.io import fits
from astropy.wcs import WCS

FILENAME = "m95_map.fit"

with fits.open(FILENAME, mode="update") as hdul:
    hdr = hdul[0].header

    wcs = WCS(hdr)

    # Extract the CD matrix
    cd = wcs.pixel_scale_matrix

    # Compute scales
    cdelt1 = (cd[0, 0] ** 2 + cd[0, 1] ** 2) ** 0.5
    if cd[0, 0] < 0:
        cdelt1 = -cdelt1
    cdelt2 = (cd[1, 0] ** 2 + cd[1, 1] ** 2) ** 0.5

    # Rotation
    import numpy as np

    # ChapGPT crota2 = np.degrees(np.arctan2(cd[1, 0], -cd[1, 1]))
    crota2 = np.degrees(np.arctan2(-cd[1, 0], cd[1, 1]))

    # Remove CD keywords
    for key in ["CD1_1", "CD1_2", "CD2_1", "CD2_2"]:
        hdr.pop(key, None)

    hdr["CDELT1"] = cdelt1
    hdr["CDELT2"] = cdelt2
    hdr["CROTA2"] = crota2

    hdul.flush()
    