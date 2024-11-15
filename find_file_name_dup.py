import os
import sys
import csv


folder_path = 'D:\\dragomans_unprocessed'

def find_duplicates(folder):
    file_names = {}  # Dictionary to store file names and their paths
    duplicates = []  # List to store duplicate file information

    def recursive_search(current_folder):
        # Iterate over all files and subdirectories in the current folder
        for item in os.listdir(current_folder):
            item_path = os.path.join(current_folder, item)

            if os.path.isdir(item_path):
                # If the item is a directory, recurse into it
                recursive_search(item_path)
            else:
                # If the item is a file, check if it already exists in the dictionary
                if item in file_names:
                    # If it exists, it's a duplicate
                    duplicates.append((item, file_names[item], item_path))
                else:
                    # Otherwise, store the file name and its path
                    file_names[item] = item_path

    # Start recursive search from the given folder
    recursive_search(folder)
    i = 1
    dupe_list = []
    # If duplicates were found, print them
    if duplicates:
        for name, original, duplicate in duplicates:
            dupe_list.append({'File_name': name, 'Original': original, 'Duplicate': duplicate, 'Index': i})
            i+=1
    if dupe_list == []:
        print('all clear!')
    return dupe_list

def check_dupe_folder(list):
    i = 1
    dupe_folders = []
    for dict in list:
        # Specify the directory path
        orig_dir = os.path.dirname(dict['Original'])
        dupe_dir = os.path.dirname(dict['Duplicate'])

        # List all files and directories
        orig_dir_file_list = os.listdir(orig_dir)
        dupe_dir_file_list = os.listdir(dupe_dir)

        # Filter to get only files in both directories (optional)
        orig_dir_file_only = set([f for f in orig_dir_file_list if os.path.isfile(os.path.join(orig_dir, f))])
        dupe_dir_file_only = set([f for f in dupe_dir_file_list if os.path.isfile(os.path.join(dupe_dir, f))])
        dupe_tuple = (orig_dir, dupe_dir)

        # if the folder of the original file has the same filenames (in terms of both quantity and name) as the duplicate
        # then mark the two folders as a pair and store them for further analysis
        # make sure all tuples in the list are distinct
        if orig_dir_file_only == dupe_dir_file_only and dupe_tuple not in dupe_folders:
            dupe_folders.append(dupe_tuple)
            print(i)
            i+=1
    return dupe_folders


find_duplicates(folder_path)
# dupe_folders = check_dupe_folder(dupe_list)
# file_path = 'duplicates_list_2.txt'

# Write the list of tuples to the CSV file
# with open(file_path, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(dupe_folders)