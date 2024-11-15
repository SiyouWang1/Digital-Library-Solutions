import cv2
import numpy as np

# Load the image
image = cv2.imread('00452!!!126 II - IMG_17069.JPG')
blurred = cv2.GaussianBlur(image, (61, 61), 0)
h, w, _ = np.shape(blurred)
padding = (h + w) // 20
top, bottom, left, right = padding, padding, padding, padding

# Add black padding (pixel value 0) around the image
black_padded_image = cv2.copyMakeBorder(blurred, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
black_padded_image = cv2.cvtColor(black_padded_image, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(black_padded_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
height, width = np.shape(binary_image)
opening_width = (height + width) // 100
# Create a kernel of size 50x50 for dilation and erosion
kernel1 = np.ones((opening_width, opening_width), np.uint8)
eroded_image = cv2.erode(binary_image, kernel1, iterations=1)
dilated_image = cv2.dilate(eroded_image, kernel1, iterations=1)

kernel2 = np.ones((opening_width * 4, opening_width * 4), np.uint8)
dilated_image = cv2.dilate(dilated_image, kernel2, iterations=1)
dilated_image = cv2.erode(dilated_image, kernel2, iterations=1)
height, width, color = np.shape(image)
# Convert to grayscale
edges = cv2.Canny(dilated_image, 50, 120)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
biggest_contour = max(contours, key=cv2.contourArea)
biggest_contour_area = cv2.contourArea(biggest_contour)
large_contours = [c for c in contours if cv2.contourArea(c) > biggest_contour_area // 3]
# Draw contours on the original image
# Convert binary image back to BGR for contour drawing
copy = cv2.cvtColor(dilated_image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(copy, large_contours, -1, (0, 255, 0), 2)

# Draw all large contours on the original binary image
binary_image_colored = cv2.cvtColor(dilated_image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(binary_image_colored, contours, -1, (0, 255, 0), 2)
cv2.imwrite('Contours.JPG', binary_image_colored)
cv2.imwrite('Copy.JPG', copy)