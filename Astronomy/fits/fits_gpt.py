import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import PercentileInterval, AsinhStretch
import numpy as np

# 1. Load the FITS cube
with fits.open("images/helix.fit") as hdul:
    data = hdul[0].data  # Shape is usually (3, Y, X)

# 2. Check and reshape the array if necessary
# Matplotlib expects the shape to be (Y, X, 3) for RGB images
if data.shape[0] == 3:
    data = np.moveaxis(data, 0, -1)

# 3. Apply a stretch/scaling so it looks good (optional but recommended)
# High dynamic range FITS data needs to be scaled between 0 and 1
interval = PercentileInterval(99.5)  # Clips extreme bright pixels
stretch = AsinhStretch()  # Brings out faint details

# Scale each channel independently
rgb_scaled = np.zeros_like(data, dtype=float)
for i in range(3):
    channel = data[:, :, i]
    # Apply normalization and stretch
    vmin, vmax = interval.get_limits(channel)
    channel_norm = np.clip((channel - vmin) / (vmax - vmin), 0, 1)
    rgb_scaled[:, :, i] = stretch(channel_norm)

# 4. Display the image
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(rgb_scaled, origin="lower")
ax.axis("off")
plt.show()
