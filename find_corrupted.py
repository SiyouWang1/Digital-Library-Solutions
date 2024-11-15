# some files are corrupted. Detect and copy those corrupted files for further analysis and processing

from PIL import Image
import os
import shutil

# Path to the directory containing images
directory_path = 'C:\\D\\DSU\\Dragomans\\upright - Copy'
corrupted_list = 'C:\\D\\DSU\\Dragomans'

counter = 1
# Loop through all files in the directory
for filename in os.listdir(directory_path):
    print(counter)
    counter += 1
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.tif', '.JPG', 'JPEG')):
        file_path = os.path.join(directory_path, filename)
        corrupted_path = os.path.join(corrupted_list, filename)
        try:
            # Try to open the image
            with Image.open(file_path) as img:
                img.verify()  # Verify the image is not corrupted
        except (IOError, SyntaxError) as e:
            # If an error occurs, add the image to the corrupted list
            shutil.move(file_path, corrupted_path)