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


def get_calibration_constants(df, mag="VMag"):
    magcat = mag + "Cat"
    x = df["BMag"] - df["VMag"]
    y = df[mag] - df[magcat]
    gradient, intercept, _, _, _ = stats.linregress(x, y)
    return gradient, intercept


def apply_calibration_constants(df, grad, inter, mag="VMag"):
    magcal = mag + "Cal"
    x = df["BMag"] - df["VMag"]
    delta = x * grad + inter
    df[magcal] = df[mag] - delta
    return df


def calibrate(df, mag="VMag"):
    gradient, intercept = get_calibration_constants(df, mag)
    df = apply_calibration_constants(df, gradient, intercept, mag)
    return gradient, intercept, df


if __name__ == "__main__":
    if len(argv) != 4:
        print(f"Usage: {argv[0]} v_stars.csv b_stars.csv catalog_stars.csv")
        exit()

    # Read the CSV files
    v_df = pd.read_csv(argv[1])
    b_df = pd.read_csv(argv[2])
    cat_df = pd.read_csv(argv[3])

    # Match V and B stars
    BGNOISE = 0.0004
    THRESHOLD = 7 * BGNOISE
    vsel = (v_df["VA"] < 1.0) & (v_df["VA"] > THRESHOLD)
    bsel = (b_df["BA"] < 1.0) & (b_df["BA"] > THRESHOLD)
    vb_df = su.match_stars(v_df[vsel], b_df[bsel], {"BA", "BMag"})
    print(f"\nTotal number of V stars: {len(v_df)}")
    print(f"Number of matched VB stars: {len(vb_df)}")

    # Match VB stars to calalog
    sel = np.isnan(cat_df["VMagCat"]) + np.isnan(cat_df["BMagCat"])
    matched_df = su.match_stars(vb_df, cat_df[~sel], {"VMagCat", "BMagCat"})
    print(f"Total number of catalog stars: {len(cat_df)}")
    print(f"Number of VB stars matched to catalog: {len(matched_df)}\n")

    # Calibrate the matched stars and calculate the calibration residuals
    vgradient, vintercept, matched_df = calibrate(matched_df, "VMag")
    vresidual = matched_df["VMagCal"] - matched_df["VMagCat"]
    print(
        f"Calibration V:   gradient={vgradient:.3f}   intercept={vintercept:.3f}   residual={vresidual.mean():.3f}+/-{vresidual.std():.3f}"
    )
    bgradient, bintercept, matched_df = calibrate(matched_df, "BMag")
    bresidual = matched_df["BMagCal"] - matched_df["BMagCat"]
    print(
        f"Calibration B:   gradient={bgradient:.3f}   intercept={bintercept:.3f}   residual={bresidual.mean():.3f}+/-{bresidual.std():.3f}\n"
    )

    # Apply the calibration constrants to all VB stars
    vb_df = apply_calibration_constants(vb_df, vgradient, vintercept, "VMag")
    vb_df = apply_calibration_constants(vb_df, bgradient, bintercept, "BMag")

    # Save to a new CSV file
    vb_df.to_csv("calibrated_vb_stars.csv", index=False)

    # Print results
    vmag = vb_df["VMagCal"]
    magva = 2.5 * np.log10(vb_df["VA"])
    vsel = vb_df["VA"] < 8 * BGNOISE
    vlim = vmag[vsel]
    valim = magva[vsel]
    print(
        f"Limiting magnitude V: {vlim.median():.3f}+/-{vlim.std():.3f}   Magnitude V range: {abs(valim.median()):.3f}   for {len(vlim)} stars"
    )

    bmag = vb_df["BMagCal"]
    magba = 2.5 * np.log10(vb_df["BA"])
    bsel = vb_df["BA"] < 13 * BGNOISE
    blim = bmag[bsel]
    balim = magba[bsel]
    print(
        f"Limiting magnitude B: {blim.median():.3f}+/-{blim.std():.3f}   Magnitude B range: {abs(balim.median()):.3f}   for {len(blim)} stars\n"
    )

    # Plot results
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(6, 9))
    fig.suptitle("Globular cluster M22")
    ax1.hist(vresidual, color="green", label="VMag-VMagCat")
    ax1.hist(bresidual, color="blue", alpha=0.5, label="BMag-BMagCat")
    ax1.legend()
    ax1.set(xlabel="$\\Delta$m")

    x = matched_df["BMag"] - matched_df["VMag"]
    ax2.plot(x, vresidual, "og")
    ax2.plot(x, bresidual, "ob", alpha=0.33)
    ax2.set(xlabel="BMag-VMag", ylabel="$\\Delta$m")
    ax2.grid()

    ax3.plot(vmag, magva, "og", alpha=0.25)
    ax3.plot(bmag, magba, "ob", alpha=0.25)
    ax3.set(xlabel="Calibrated Mag", ylabel="2.5*log10(A)")
    ax3.grid()

    plt.show()
