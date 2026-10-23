#!/usr/bin/env python3
"""
HR diagram
"""

from sys import argv
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import star_utils as su


def calibrate_magnitude(xx, yy):
    gradient, intercept, _, _, _ = stats.linregress(xx, yy)
    print(f"Magnitude gradient: {gradient:.3f}   Magnitude intercept: {intercept:.3f}")
    delta = xx * gradient + intercept
    return delta


if __name__ == "__main__":
    if len(argv) != 4:
        print(f"Usage: {argv[0]} b_stars.csv v_stars.csv catalog_stars.csv")
        exit()

    # Read the CSV files
    b_df = pd.read_csv(argv[1])
    v_df = pd.read_csv(argv[2])
    cat_df = pd.read_csv(argv[3])

    # Match B and V stars
    matched_df = su.match_stars(b_df, v_df, {"VMag"})
    print(f"\nTotal number of V stars: {len(v_df)}")
    print(f"Number of matched BV stars: {len(matched_df)}")

    # Match BV stars to calalog
    matched_df = su.match_stars(matched_df, cat_df, {"VMagCat", "BMagCat"})
    print(f"Total number of catalog stars: {len(cat_df)}")
    print(f"Number of BV stars with selections and matched to catalog: {len(matched_df)}")

    # Apply quality selections
    BGNOISE = 0.0004
    THRESHOLD = 7 * BGNOISE
    selection = (matched_df["A"] < 1.0) & (matched_df["A"] > THRESHOLD)
    vmag = matched_df["VMagCat"][selection]
    bmag = matched_df["BMagCat"][selection]
    my_vmag = matched_df["VMag"][selection]
    my_bmag = matched_df["BMag"][selection]

    # Calibrate the V magnitudes
    x = my_bmag - my_vmag
    y = my_vmag - vmag
    voffsets = calibrate_magnitude(x, y)
    mean = (y - voffsets).mean()
    sigma = (y - voffsets).std()
    print(f"V magnitude calibration: {mean:.3f} +/- {sigma:.3f}")

    # Calibrate the B magnitude
    y = my_bmag - bmag
    boffsets = calibrate_magnitude(x, y)
    mean = (y - boffsets).mean()
    sigma = (y - boffsets).std()
    print(f"B magnitude calibration: {mean:.3f} +/- {sigma:.3f}")
    print("\n")

    # Apply the magnitude calibrations
    my_vmag -= voffsets
    my_bmag -= boffsets

    fig, (ax1, ax2) = plt.subplots(2, figsize=(6, 9))
    fig.suptitle("Globular cluster M22")
    ax1.hist(my_bmag - bmag, label="B-Bcat")
    ax1.hist(my_vmag - vmag, color="C1", alpha=0.5, label="V-Vcat")
    ax1.legend()
    ax1.set(xlabel="$\\Delta$m")
    ax2.plot(my_bmag - my_vmag, -my_vmag, "ob", alpha=0.25)[0].set_label("Iouri")
    ax2.plot(bmag - vmag, -vmag, "or", alpha=0.25)[0].set_label("Simbad")
    ax2.set(xlabel="B-V", ylabel="-V")
    ax2.grid()
    ax2.legend()
    plt.show()
