import numpy as np
import cv2

# Create an all-black empty image (filled with zeros)
image = np.zeros((5000, 5000), dtype=np.uint8)

def draw_line(theta, dist, image):
    # Calculate slope and y-intercept from theta and distance
    y_intercept = dist / np.sin(theta)
    slope = - np.cos(theta) / np.sin(theta)
    
    # Find two points to draw the line across the image dimensions
    x0, y0 = 0, int(y_intercept)  # Point at x = 0
    x1, y1 = image.shape[1] - 1, int(slope * (image.shape[1] - 1) + y_intercept)  # Point at max x
    
    # Use OpenCV's line function to draw the line
    cv2.line(image, (x0, y0), (x1, y1), 255, 1)

# Iterate to draw multiple lines
for i in range(0, 1250):
    draw_line(np.radians(7), i * 4, image)

# Save the resulting image
cv2.imwrite('result.jpg', image)