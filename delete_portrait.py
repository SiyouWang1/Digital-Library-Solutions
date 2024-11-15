import os
from PIL import Image
import shutil

# Define the folder containing the images
image_folder = "C:\\D\\DSU\\Dragomans\\upright-corrected"
result_folder = 'C:\\D\\DSU\\Dragomans\\upright-corrected\\two-page'

# Loop through all files in the folder
for filename in os.listdir(image_folder):
    file_path = os.path.join(image_folder, filename)

    # Ensure the file is an image (add more extensions if needed)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        try:
            # Open the image
            with Image.open(file_path) as img:
                # Get the dimensions of the image
                width, height = img.size

            # Check if the image is in portrait mode (height > width)
            if height < width:
                print(f"Landscape image detected: {filename}")
                shutil.move(file_path, result_folder)
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")