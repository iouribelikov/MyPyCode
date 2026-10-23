#!/usr/bin/env python3
"""
This script shows one-by-one FITs given on the invokation command line
"""

from sys import argv
import numpy as np

import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style

plt.style.use(astropy_mpl_style)


def plot():
    with fits.open(file) as hdul:
        hdul.info()
        header = hdul[0].header
        print(repr(header))

        #        header["OBJECT"] = "M33"
        #        header.comments["OBJECT"] = "Triangulum galaxy"
        #        fits.writeto("output_file.fits", img, header)

        img = hdul[0].data
        if len(img.shape) == 3:
            img = np.transpose(img, (1, 2, 0))
        plt.figure()
        plt.imshow(img, origin="lower", cmap="gray")
        plt.colorbar()
        plt.show(block=False)
        plt.pause(3)  # 3 sec


if len(argv) < 2:
    print("Please, provide a file name !")
    exit()
for file in argv[1:]:
    plot()
