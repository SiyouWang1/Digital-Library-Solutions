import os
import shutil

# Paths to the two folders
src_folder = 'C:\\D\\DSU\\Dragomans\\upright-corrected, two-page separated'  # The folder containing 10000 files without structure
target_folder = 'D:\\.....Special_media_images\\dragomans_unprocessed_enumerated'  # The folder with the desired folder structure

def replicate_structure(src_folder, target_folder):
    missing_list = []
    # Walk through all files and directories in the target_folder
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            # Get the relative path of the file from the target folder root
            relative_path = os.path.relpath(os.path.join(root, file), target_folder)
            
            # Create the corresponding directory structure in the source folder
            target_dir = os.path.join(src_folder, os.path.dirname(relative_path))
            os.makedirs(target_dir, exist_ok=True)
            
            nm, ext = os.path.splitext(file)
            # Source file path (without structure) and new target file path (with structure)
            src_file_path = os.path.join(src_folder, file)
            src_file_path_left = os.path.join(src_folder, nm + 'left' + ext)
            src_file_path_right = os.path.join(src_folder, nm + 'right' + ext)
            new_file_path = os.path.join(target_dir, file)
            new_file_path_left = os.path.join(target_dir, nm + 'left' + ext)
            new_file_path_right = os.path.join(target_dir, nm + 'right' + ext)
            
            # Move the file from src_folder to the new location
            found = False
            if os.path.exists(src_file_path):
                shutil.move(src_file_path, new_file_path)
                found = True
            if os.path.exists(src_file_path_left):
                shutil.move(src_file_path_left, new_file_path_left)
                found = True
            if os.path.exists(src_file_path_right):
                shutil.move(src_file_path_right, new_file_path_right)
                found = True
            if not found:
                missing_list.append(src_file_path)

    # Get the current directory of the .py file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the filename and full path for the new text file
    txt_name = "missing_list_.txt"
    txt_path = os.path.join(current_dir, txt_name)

    # Write the list to the text file
    with open(txt_path, 'w') as file:
        for item in missing_list:
            file.write(f"{item}\n")

# Call the function with the paths to your folders
replicate_structure(src_folder, target_folder)