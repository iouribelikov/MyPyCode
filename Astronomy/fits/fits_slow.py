#!/usr/bin/env python3
"""
This script does not work with grey-scale images !
"""

import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np

# from astropy.visualization import make_lupton_rgb

plt.style.use(astropy_mpl_style)

with fits.open("images/m95_rgb.fit") as hdul:
    hdul.info()
    hdr = hdul[0].header
    print(repr(hdr))
    data = hdul[0].data
    n, x, y = data.shape

r = np.reshape(data[0], x * y)
g = np.reshape(data[1], x * y)
b = np.reshape(data[2], x * y)

img = []
for i in range(x * y):
    img.append([r[i], g[i], b[i]])


img = np.reshape(img, (x, y, n))

plt.figure()
plt.imshow(img, origin="lower", cmap="gray", vmin=0.002, vmax=0.012)
plt.colorbar()
plt.show()
