# Extract the text orientation in the pytesseract osd info
# Too slow and not reliable
# the Orientation property in the OSD data is in terms of clockwise rotation
# PIL Image rotates counterclockwise

import pytesseract
import cv2
import numpy as np
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

# Load the image
image = cv2.imread('0000013.TIF')
# sharpening_kernel = np.array([[0, -1, 0],
#                               [-1, 5, -1],
#                               [0, -1, 0]])

# # Apply the kernel to the image using cv2.filter2D
# image = cv2.filter2D(image, -1, sharpening_kernel)
y, x, _ = np.shape(image) 
print(f"x: {x}, y: {y}")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a Gaussian blur to smooth the image and remove small details
# blurred = cv2.GaussianBlur(gray, (3, 3), 0)
blurred = cv2.bilateralFilter(gray, d=21, sigmaColor=40, sigmaSpace=75)

# Resize Image
resized = cv2.resize(blurred, (int(900 / y * x), 900))

# Apply thresholding
_, binary = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# Close the shape to eliminate any contours from texts
# kernel0 = np.ones((5, 5), np.uint8)
# dilated_image = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel0)
dilated_image = cv2.resize(binary, (int(900 / y * x), 900))
cv2.imwrite('binary.jpg', binary)

# Display the image in a window
cv2.imshow('Corrected', resized)
cv2.imshow('Bin', dilated_image)

# Wait indefinitely until a key is pressed
cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()
# image90 = image.rotate(90)
# image180 = image.rotate(180)
# image270 = image.rotate(270)

# Get orientation and script detection (OSD) information config = '--oem 1 -l tam --psm 0'
osd_info = pytesseract.image_to_osd(binary, lang = 'tam')
# osd_info1 = pytesseract.image_to_osd(image90)
# osd_info2 = pytesseract.image_to_osd(image180)
# osd_info3 = pytesseract.image_to_osd(image270)

print(osd_info)
# print(osd_info1)
# print(osd_info2)
# print(osd_info3)