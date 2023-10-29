#!/usr/bin/env python3
#
# This file is part of the droplet analysis scripts.
#
# Copyright (c) 2023 Jason Toney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""docstring goes here"""


import os
import sys
import csv
import matplotlib.pyplot as plt


def summarize_droplet_sizes(csv_file_path):
    """docstring goes here"""
    # image title
    image_name = os.path.splitext(os.path.basename(csv_file_path))[0].split("_")[2:-1][
        0
    ]
    # Initialize a dictionary to store the summary
    summary = {}
    # Define the bin size for summarizing in increments of 10 microns
    bin_size = 10
    # Count all ROIs
    total_rois = 0
    # Read the CSV file
    with open(csv_file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        # Process each row in the CSV
        for row in reader:
            # Calculate the bin for the current value
            bin_number = int(float(row["Feret"]) // bin_size)
            # Update the count for the corresponding bin
            summary[bin_number] = summary.get(bin_number, 0) + 1
            total_rois += 1

    # Sort the summary dictionary by bin number
    sorted_summary = dict(sorted(summary.items()))

    # Write the summary to a new CSV file
    with open(f"results/{image_name}.csv", "w", newline="") as csvfile:
        fieldnames = ["Bin (microns)", "Count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for bin_number, count in sorted_summary.items():
            bin_start = bin_number * bin_size
            bin_end = (bin_number + 1) * bin_size
            writer.writerow({"Bin (microns)": f"{bin_start}-{bin_end}", "Count": count})

    print(f"Droplet size summary has been written to {image_name}.csv")
    print(f"Recorded {total_rois} total ROIs")

    # Extract the data for plotting
    bins = [bin_num * bin_size for bin_num in sorted_summary.keys()]
    counts = list(sorted_summary.values())

    # Create the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(bins, counts, width=bin_size, align="edge", edgecolor="black")
    plt.xlabel("Droplet Feret Diameter (microns)")
    plt.ylabel("Count")
    plt.title(f"{image_name} - Droplet Size Summary")
    plt.grid(axis="y")
    plt.savefig(f"results/{image_name}.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    # Check if the user provided the CSV file path in the command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_droplets.py <csv_file_path>")
        sys.exit(1)

    # Get the CSV file path from command-line arguments
    summarize_droplet_sizes(sys.argv[1])
