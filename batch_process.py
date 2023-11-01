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

"""
    This script executes the ImageJ macro and python scripts in a batch process.
    Input: all images found within the local "ECHO Images" folder.
    Output: CSV file containing the total droplet counts binned by size.
"""


import os
import subprocess
import sys
import time
import zipfile

import analyze_droplets
import compile_workbook


def batch_process(image_folder):
    """Analyze all the image albums found in "ECHO Images" subdirectories."""
    # Start the timer
    start_time = time.time()
    # Count how many images are processed
    processed = 0

    # Work inside the ImageJ directory
    os.chdir(f"{os.path.dirname(__file__)}/ImageJ")
    # Iterate through the image folders
    for folder_name in os.listdir(image_folder):
        # Full path to the current image folder
        current_folder = os.path.join(image_folder, folder_name)

        # Check if the current item is a directory
        if os.path.isdir(current_folder):
            # remove unnecessary extraneous files
            for file in os.listdir(current_folder):
                if not (file.startswith("Tile0") and file.endswith(".jpg")):
                    os.remove(f"{current_folder}/{file}")

            print(f"Processing folder: {current_folder}")
            processed += 1
            # Execute the ImageJ macro for the current folder
            command = [
                "./ImageJ.exe",
                "-macro",
                "droplets/AnalyzeDroplets.ijm",
                current_folder,
            ]

            try:
                subprocess.run(command, capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as exception:
                print(f"Error executing the macro: {exception}")

    # Process the ImageJ results
    os.chdir(os.path.dirname(__file__))
    for file in os.listdir("ImageJ/droplets/results"):
        if file.endswith(".csv"):
            analyze_droplets.summarize_droplet_sizes(f"ImageJ/droplets/results/{file}")

    # Compile the results into a workbook
    compile_workbook.main()

    # Zip the images
    with zipfile.ZipFile("DropletSize_Charts.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("results"):
            for file in files:
                if file.endswith((".png")):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, "results")
                    zipf.write(file_path, arcname)

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    # Print elapsed time in H:M:S format
    print(f"\nElapsed time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}")
    print(f"Images processed: {processed}")
    input("Batch processing complete. Press ENTER.\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        IMAGE_FOLDER = sys.argv[1]
    else:
        IMAGE_FOLDER = "../ECHO Images"
    batch_process(IMAGE_FOLDER)
