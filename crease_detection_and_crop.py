import cv2
import os
import numpy as np

src = 'C:\\D\\DSU\\Dragomans\\upright-corrected, two-page separated\\two-page'
output = 'C:\\D\\DSU\\Dragomans\\upright-corrected, two-page separated\\two-page-splitted'

def split_in_two(filepath, name):
    # Load the image and pre-process it
    image = cv2.imread(filepath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 100, apertureSize=3)

    # Get image dimensions
    _, width = edges.shape

    # Define the middle sixth region so that crease detection is limited in this region
    start_x = width // 12 * 5 
    end_x = width // 12 * 7

    min_boundary_pixels = float('inf')  # Initialize the amount of crossed boundary pixles to infinity
    best_x = start_x  # Initialize the best x to the start of the middle fifth

    # Iterate through vertical lines in the middle sixth
    for x in range(start_x, end_x):
        # Count the number of boundary pixels this vertical line passes through
        boundary_pixels = np.sum(edges[:, x])

        # Update the best line if the current one passes through fewer boundary pixels
        if boundary_pixels < min_boundary_pixels:
            min_boundary_pixels = boundary_pixels
            best_x = x
    left_page = image[:, :int(best_x)]
    right_page = image[:, int(best_x):]

    nm, ext = os.path.splitext(name)
    left_name = nm + 'left' + ext
    right_name = nm + 'right' + ext
    left_path = os.path.join(output, left_name)
    right_path = os.path.join(output, right_name)

    # Save the resulting sliced images
    cv2.imwrite(left_path, left_page, [cv2.IMWRITE_JPEG_QUALITY, 100])
    cv2.imwrite(right_path, right_page, [cv2.IMWRITE_JPEG_QUALITY, 100])

for filename in os.listdir(src):
    imgpath = os.path.join(src, filename)
    if filename.endswith(('.jpg', '.jpeg', '.JPEG', '.JPG', '.png', '.gif', '.tif', 'PNG')):
        split_in_two(imgpath, filename)
        print(filename)