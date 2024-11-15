# This script uses the rotation data recorded in the CSV
# file to correct the rotation of the images in certain
# folders.

from PIL import Image, ImageOps
import os
import cv2
import time
import pandas as pd
import numpy as np

src = 'C:\\D\\DSU\\Kanagaratnam\\test_rotation\\80_INTERNATIONAL TAMIL\'S ARCHIVES KANDY_ TO'
dst = 'C:\\D\\DSU\\Kanagaratnam\\test_rotation\\Corrected\\80'

df = pd.read_csv('Kanagaratanam - UTSC microfilm reels - Rotate.csv')
# df = df[df['Original Reel'].isin([80])]
df = df.reset_index(drop = True)
df = df[['Original Reel', 'Filenumber', 'Rotation']]

start_time = time.time()
filenum = df['Filenumber'].unique()
rotations = df['Rotation'].unique()

# Write filenum and rotations to a text file
output_file = 'filenum_rotations.txt'
with open(output_file, 'w') as f:
    f.write("Filenumbers:\n")
    for fn in filenum:
        f.write(f"{fn}\n")
    f.write("\nRotations:\n")
    for rot in rotations:
        f.write(f"{rot}\n")

print(f"Data written to {output_file}")
end_time = time.time()
time_length = end_time - start_time
print(time_length)