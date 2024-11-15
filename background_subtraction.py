import cv2
import numpy as np


image = cv2.imread('00452!!!126 II - IMG_17069.JPG')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a Gaussian blur to smooth the image and remove small details
blurred = cv2.GaussianBlur(gray, (51, 51), 0)
blurred = blurred // 255

# Subtract the blurred image from the original
illumination_corrected = cv2.subtract(gray, blurred)
illumination_corrected = cv2.resize(illumination_corrected, (1600, 900))

# Apply Otsu's thresholding
_, binary = cv2.threshold(illumination_corrected, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
binary = cv2.resize(binary, (1600, 900))

# Display the image in a window
cv2.imshow('Corrected', illumination_corrected)
cv2.imshow('Bin', binary)

# Wait indefinitely until a key is pressed
cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()