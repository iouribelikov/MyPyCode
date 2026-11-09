#!/usr/bin/env python3
"""
Calibrate the magnitude
"""

from argparse import ArgumentParser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import star_utils as su

if __name__ == "__main__":
    parser = ArgumentParser(
        # prog="calibrate_magnitude.py",
        description="Description of the program",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("my_stars_csv", metavar="my_stars.csv", help="file with my stars")
    parser.add_argument("cat_stars_csv", metavar="cat_stars.csv", help="file with catalog stars")
    parser.add_argument(
        "-bg", "--background", type=float, default=0.0, help="background value [0,1]"
    )
    parser.add_argument(
        "-bgnoise",
        "--background_noise",
        type=float,
        default=2.0e-4,
        help="background noise value [0,1]",
    )
    args = parser.parse_args()
    # print(args)

    # Read the CSV files
    v_df = pd.read_csv(args.my_stars_csv)
    cat_df = pd.read_csv(args.cat_stars_csv)

    # Match stars
    sel = np.isnan(cat_df["VMagCat"])
    matched_df = su.match_stars(v_df, cat_df[~sel], {"VMagCat", "BMagCat"})

    # Calculate the magnitude offset
    THRESHOLD_LOW = 7 * args.background_noise
    THRESHOLD_UP = 1 - args.background
    selection1 = (matched_df["VA"] < THRESHOLD_UP) & (matched_df["VA"] > THRESHOLD_LOW)
    deltaVMag = (matched_df["VMag"] - matched_df["VMagCat"])[selection1]

    voffset = deltaVMag.mean()
    offset = deltaVMag.mean()
    sigma = deltaVMag.std()

    matched_df["VMag"] -= offset
    v_df["VMag"] -= offset

    # Save to a new CSV file
    matched_df.to_csv("matched_stars.csv", index=False)

    selection2 = (v_df["VA"] < THRESHOLD_UP) & (v_df["VA"] > THRESHOLD_LOW)
    mag = v_df[selection2]["VMag"]
    a = v_df[selection2]["VA"]
    maga = 2.5 * np.log10(a)
    vsel = v_df["VA"] < THRESHOLD_LOW + args.background_noise
    vlim = mag[vsel]
    mrange = maga.max() - maga.min()
    effective = mrange / (2.5 * np.log10(THRESHOLD_UP / THRESHOLD_LOW)) * 100

    # Print results
    print(f"\nTotal number of my stars: {len(v_df)}")
    print(f"Total number of catalog stars: {len(cat_df)}")
    print(f"Number of my stars matched to catalog: {len(matched_df)}\n")
    print(f"Magnitude calibration offset: {offset:.3f} +/- {sigma:.3f}")
    print(
        f"Magnitude V range: {mrange:.3f} ({effective:.1f}% of effective)   Limiting magnitude V: {vlim.median():.3f}+/-{vlim.std():.3f}   for {len(vlim)} stars\n"
    )

    # Plot results
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(6, 9))
    fig.suptitle("Globular cluster M22")
    ax1.hist(deltaVMag, label="VMagCat-VMag")
    ax1.legend()
    ax1.set(xlabel="$\\Delta$m")
    ax2.plot(matched_df["VMagCat"][selection1], matched_df["VMag"][selection1], "or")
    ax2.set(xlabel="VMagCat", ylabel="VMag")
    ax2.grid()
    ax3.plot(mag, maga, "ob", alpha=0.25)
    ax3.set(xlabel="Calibrated VMag", ylabel="2.5*log10(A)")
    ax3.grid()

    plt.show()
