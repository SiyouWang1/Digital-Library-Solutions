# find the desired rotation correction value according to the general skew of texts in the image

import cv2
import numpy as np
import os
path = 'D:\\...Special_media_image_processing\\Dragomans\\Small_test'

def rotate_all(imagepath, imgname):
    image = cv2.imread(imagepath)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection to detect edges in the image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Apply Hough Line Transform to detect lines
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    # Calculate the angles of the detected lines
    angles = []
    for line in lines:
        rho, theta = line[0]
        angle = np.degrees(theta) - 90  # Adjust angle to align with horizontal lines
        angles.append(angle)

    # Find the median angle of the lines
    if len(angles) > 0:
        skew_angle = np.median(angles)
    else:
        # Default to no rotation if no lines found
        skew_angle = 0  

    # Make sure the angle is positive
    while skew_angle < 0:
        skew_angle += 360

    print(skew_angle)

    # round the detected rotation to multiples of 90 degrees
    if 45 <= skew_angle < 135:
        rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif 135 <= skew_angle < 225:
        rotated = cv2.rotate(image, cv2.ROTATE_180)
    elif 225 <= skew_angle < 315:
        rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    else:
        rotated = image

    # Output the rotated image
    cv2.imwrite(imagepath, rotated)

for filename in os.listdir(path):
    if filename.endswith(('.png', '.jpg', 'gif', 'tif', 'JPG')):
        imgpath = os.path.join(path, filename)
        rotate_all(imgpath, filename)