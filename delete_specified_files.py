# This code delete the list of images/files according to a list stored in a csv file

import csv
import os

# Path to your CSV file
csv_file_path = 'Unprocessed File List - Duplicate Filepaths.csv'  # Replace with your actual CSV file path

# Read the CSV file and delete each file
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    # Iterate over each row in the CSV file
    for row in csv_reader:
        file_path = row[0]  # Assuming file path is in the first column
        true_path = 'F:/.....Special_media_images' + file_path[30:]

        # Check if the file exists before trying to delete it
        if os.path.exists(true_path):
            try:
                os.remove(true_path)
                print(f"Deleted: {true_path}")
            except Exception as e:
                print(f"Error deleting {true_path}: {e}")
        else:
            print(f"File not found: {true_path}")