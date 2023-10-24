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
import time
import zipfile

import analyze_droplets
import compile_workbook


def batch_process(image_folder):
    """docstring goes here"""
    # Start the timer
    start_time = time.time()
    # Count how many images are processed
    processed = 0

    # Process the ImageJ results
    os.chdir(os.path.dirname(__file__))
    for file in os.listdir("ImageJ/droplets/results"):
        if file.endswith(".csv"):
            analyze_droplets.summarize_droplet_sizes(
                f"ImageJ/droplets/results/{file}"
            )

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
    os.chdir(f"{os.path.dirname(sys.argv[0])}/ImageJ")
    if len(sys.argv) > 1:
        IMAGE_FOLDER = sys.argv[1]
    else:
        IMAGE_FOLDER = "../ECHO Images"
    batch_process(IMAGE_FOLDER)
