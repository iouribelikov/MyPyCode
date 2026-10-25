#!/usr/bin/env python3
"""
HR diagram
"""

from sys import argv
import pandas as pd
import matplotlib.pyplot as plt
import star_utils as su

if __name__ == "__main__":
    if len(argv) != 3:
        print(f"Usage: {argv[0]} calibrated_vb_stars.csv catalog_stars.csv")
        exit()

    # Read the CSV files
    vb_df = pd.read_csv(argv[1])
    cat_df = pd.read_csv(argv[2])
    cat_label = "Simbad"

    # print("Converting the Gaia spectral information to V and B...")
    # cat_df = su.gaia_to_vb(cat_df)
    # cat_label = "Gaia"

    print(f"\nNumber of VB stars: {len(vb_df)}")
    print(f"Number of catalog stars: {len(cat_df)}\n")

    fig, ax = plt.subplots()
    fig.suptitle("Globular cluster M22")
    bv = vb_df["BMagCal"] - vb_df["VMagCal"]
    ax.plot(bv, -vb_df["VMagCal"], "ob", alpha=0.25)[0].set_label("Iouri")
    bv = cat_df["BMagCat"] - cat_df["VMagCat"]
    ax.plot(bv, -cat_df["VMagCat"], "or", alpha=0.15)[0].set_label(cat_label)
    ax.set(xlabel="B-V", ylabel="-V")
    ax.grid()
    ax.set_xlim([-0.5, 2.5])
    ax.set_ylim([-17.5, -10])
    ax.legend()
    plt.show()
