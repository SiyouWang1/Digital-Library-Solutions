import os

src = 'C:\\D\\DSU\\Dragomans\\upright-corrected, two-page separated'

def enumerate_prefix_to_files(base_dir):
    # Initialize prefix counter
    counter = 1
    
    # Walk through all files and directories in base_dir
    for root, _, files in os.walk(base_dir):
        for file in files:
            # Generate the five-digit prefix, zero-padded
            prefix = f"{counter:05d}"
            
            # Construct old and new file paths
            old_file_path = os.path.join(root, file)
            new_file_name = f"{prefix}!!!{file}"
            new_file_path = os.path.join(root, new_file_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            
            # Increment the counter
            counter += 1

def delete_prefix_to_files(base_dir):
    # Initialize prefix counter
    counter = 1
    # Walk through all files and directories in base_dir
    for root, _, files in os.walk(base_dir):
        for file in files:
            # Generate the five-digit prefix, zero-padded
            prefix = f"{counter:05d}"
            
            # Construct old and new file paths
            old_file_path = os.path.join(root, file)
            new_file_name = file[8:]
            new_file_path = os.path.join(root, new_file_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            
            # Increment the counter
            counter += 1
            print(counter)

# Call the function with the path to the base directory
# enumerate_prefix_to_files(src)
delete_prefix_to_files(src)