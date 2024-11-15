import cv2
import numpy as np
import os
src = 'D:\\...Special_media_image_processing\\Dragomans\\Upsidedown'

def rms_flat(a):
    # Return the root mean square of all the elements of *a*, flattened out.
    return np.sqrt(np.mean(np.abs(a) ** 2))

def project(impath):
    # Load the image and preprocess it
    image = cv2.imread(impath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edges = cv2.Canny(gray, 50, 120, apertureSize=3)

    # Demean; make the brightness extend above and below zero
    gray = gray - np.mean(gray)
    height, width = gray.shape

    # get the biggest square that fits in the middle of the image
    # and project its pixels by adding them horizontallhy or vertically
    if height > width:
        gap = (height - width) // 2
        gray = gray[gap:height-gap, :]
        x_projection = []
        for x in range(0, width - 1):
            x_projection.append(np.sum(gray[:, x]))
        x_npprojection = np.array(x_projection)
        y_projection = []
        for y in range(0, width - 1):
            y_projection.append(np.sum(gray[y, :]))
        y_npprojection = np.array(y_projection)
    else:
        gap = (width - height) // 2
        gray = gray[:, gap:width-gap]
        y_projection = []
        for y in range(0, height - 1):
            y_projection.append(np.sum(gray[y, :]))
        y_npprojection = np.array(y_projection)
        x_projection = []
        for x in range(0, height - 1):
            x_projection.append(np.sum(gray[:, x]))
        x_npprojection = np.array(x_projection)

    # use rms_flat() to decide which projection represents the upright direction
    # if x_npprojection is greater than its counterpart, then the image needs a 
    # degree rotation
    if rms_flat(x_npprojection) > rms_flat(y_npprojection):
        return False
    else:
        return True

# iterate over all images and see the success rate of this method in deciding
# the orientation of the image (horizontal or vertical)
f = 1
s = 1
for filename in os.listdir(src):
    imgpath = os.path.join(src, filename)
    print(f'the rate of success is {s / (s+f)}')
    if project(imgpath):
        s += 1
    else:
        f += 1