#!/usr/bin/env python3
"""
Compare catalogs
"""

from sys import argv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import star_utils as su

if __name__ == "__main__":
    if len(argv) != 3:
        print(f"Usage: {argv[0]} catalog1_stars.csv catalog2_stars.csv")
        exit()

    # Read the CSV files
    df1 = pd.read_csv(argv[1])
    df2 = pd.read_csv(argv[2])

    print("Converting the Gaia spectral information to V and B...")
    df2 = su.gaia_to_vb(df2)

    df2 = df2.rename(columns={"VMagCat": "VMagCat2"})

    # Match stars
    sel1 = ~np.isnan(df1["VMagCat"])
    sel2 = ~np.isnan(df2["VMagCat2"])
    matched_df = su.match_stars(df1[sel1], df2[sel2], {"VMagCat2"})

    delta = matched_df["VMagCat"] - matched_df["VMagCat2"]

    # Print results
    print(f"\nTotal number of stars in the 1st catalog: {len(df1)}")
    print(f"Total number of stars in the 2nd Catalog: {len(df2)}")
    print(f"Number of matched stars: {len(matched_df)}\n")
    print(f"Magnitude difference: {delta.mean():.3f} +/- {delta.std():.3f}")

    # Plot results
    fig, (ax1, ax2) = plt.subplots(2, figsize=(6, 9))
    ax1.hist(delta, label="VMagCat-VMagCat2")
    ax1.legend()
    ax1.set(xlabel="$\\Delta$m")
    ax2.plot(matched_df["VMagCat"], matched_df["VMagCat2"], "or")
    ax2.set(xlabel="VMagCat", ylabel="VMagCat2")
    ax2.grid()

    plt.show()
