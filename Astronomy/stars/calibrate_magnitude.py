#!/usr/bin/env python3
"""
Calibrate the magnitude
"""

from sys import argv
from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import star_utils as su

if __name__ == "__main__":
    if len(argv) != 3:
        print(f"Usage: {argv[0]} my_stars.csv catalog_stars.csv")
        exit()

    # Read the CSV files
    v_df = pd.read_csv(argv[1])
    cat_df = pd.read_csv(argv[2])

    # Match stars
    matched_df = su.match_stars(v_df, cat_df, {"VMagCat", "BMagCat"})

    # Calculate the magnitude offset
    BGNOISE = 0.0004
    THRESHOLD = 7 * BGNOISE
    selection1 = (matched_df["A"] < 1.0) & (matched_df["A"] > THRESHOLD)
    deltaVMag = (matched_df["VMag"] - matched_df["VMagCat"])[selection1]

    voffset = deltaVMag.mean()

    x = v_df["BMag"] - v_df["VMag"]
    voffset = -0.618 * x - 14.145
    v_df["VMag"] -= voffset

    x = (matched_df["BMag"] - matched_df["VMag"])[selection1]
    voffset = -0.618 * x - 14.145
    deltaVMag -= voffset
    offset = deltaVMag.mean()
    sigma = deltaVMag.std()

    selection2 = (v_df["A"] < 1.0) & (v_df["A"] > THRESHOLD)
    mag = v_df[selection2]["VMag"]
    a = v_df[selection2]["A"]
    maga = 2.5 * np.log10(a)
    mrange = abs(maga.min())

    # Print results
    print(f"\nTotal number of my stars: {len(v_df)}")
    print(f"Total number of catalog stars: {len(cat_df)}")
    print(f"Number of my stars matched to catalog: {len(matched_df)}")
    print(f"Magnitude calibration: {offset:.3f} +/- {sigma:.3f}")
    print(f"Limiting magnitude: {mag.min() + mrange:.3f}   Magnitude range: {mrange:.3f}\n")

    # Save to a new CSV file
    matched_df.to_csv("matched_stars.csv", index=False)

    # Plot results
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(6, 9))
    fig.suptitle("Globular cluster M22")
    ax1.hist(deltaVMag, label="VMagCat-VMag")
    ax1.legend()
    ax1.set(xlabel="$\\Delta$m")
    ax2.plot(matched_df["VMagCat"][selection1], matched_df["VMag"][selection1] - voffset, "or")
    ax2.set(xlabel="VMagCat", ylabel="VMag")
    ax2.grid()
    ax3.plot(mag, maga, "ob", alpha=0.25)
    ax3.set(xlabel="Calibrated VMag", ylabel="2.5*log10(A)")
    ax3.grid()

    plt.show()
