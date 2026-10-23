#!/usr/bin/env python3
"""
My first FIT visualisation script
"""

from sys import argv

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style, PercentileInterval, AsinhStretch

plt.style.use(astropy_mpl_style)

interval = PercentileInterval(99.5)  # Clips extreme bright pixels
stretch = AsinhStretch()  # Brings out faint details


def stretch_channel(channel):
    """
    stretch colour channel
    """
    vmin, vmax = interval.get_limits(channel)
    channel_norm = np.clip((channel - vmin) / (vmax - vmin), 0, 1)
    return stretch(channel_norm)


def plot(ffile):
    """
    Plotting function
    """
    with fits.open(ffile) as hdul:
        hdul.info()
        # print(repr(hdul[0].header))
        img = hdul[0].data

        rgb = len(img.shape)
        if rgb == 3:
            img = np.transpose(img, (1, 2, 0))
            for i in range(rgb):
                img[:, :, i] = stretch_channel(img[:, :, i])
        else:
            img[:, :] = stretch_channel(img[:, :])

        plt.figure()
        plt.title(hdul[0].header.get("OBJECT", "Unknown object"))
        plt.imshow(img, origin="lower", cmap="gray")
        plt.colorbar()
        # plt.show()
        plt.show(block=False)
        plt.pause(3)  # 3 sec


if __name__ == "__main__":
    if len(argv) < 2:
        print("Please, provide a file name !")
        exit()
    for file in argv[1:]:
        plot(file)
