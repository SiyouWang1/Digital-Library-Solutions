# this is the first step of the 3-step process. After this, delete the specified files, and lastly add the enumeration to all the files.
# remember, the dragomans_unprocessed folder in the F drive already have all the 1.3k files specified in the csv deleted.

import os
import shutil

def move_files_to_folder(src_root, dst_folder):
    # Create the destination folder if it doesn't exist
    counter = 1
    os.makedirs(dst_folder, exist_ok=True)
    
    # Walk through all directories and files in the source root
    for root, dirs, files in os.walk(src_root):
        for file in files:
            # Construct full file path by adding enumeration filename prefix
            prefix = f"{counter:05d}"
            src_file = os.path.join(root, file)
            new_file_name = f"{prefix}!!!{file}"
            dst_file = os.path.join(dst_folder, new_file_name)
            
            # Copy the file to the destination folder
            shutil.copy2(src_file, dst_file)
            counter += 1
            print(f"Moved {src_file} to {dst_file}")


src_root = 'F:\\.....Special_media_images\\dragomans_unprocessed'
dst_folder = 'D:\\...Special_media_image_processing\\Dragomans\\Unified'
move_files_to_folder(src_root, dst_folder)