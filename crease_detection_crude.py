import cv2
import numpy as np

# pre-process the image
image = cv2.imread('253 - IMG_1519.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

# initialize values so that I can find the vertical lines close to the center later
image_center = image.shape[1] // 2
closest_line = None
min_dist = float('inf')

# Overlay lines on the edges image
# Convert edges to BGR for color overlay
output = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

if lines is not None:
    for rho, theta in lines[:, 0]:
        # Filter out non-vertical lines in a 78 degrees region
        if -1 * np.pi / 39 < theta < 1 * np.pi / 39:  
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * a)
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * a)

            # Draw the line on the edges image
            cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Find the line closest to the center
            x_intercept = abs(rho / np.cos(theta))
            dist_from_center = abs(x_intercept - image_center)
            if dist_from_center < min_dist:
                min_dist = dist_from_center
                closest_line = x_intercept

# Save and display the image with overlaid lines
cv2.imwrite('output_with_lines.jpg', output)
cv2.waitKey(0)
cv2.destroyAllWindows()