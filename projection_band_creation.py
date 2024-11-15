# the following function projects the image by adding its pixels horizontally or vertically
# after transorming the image into its edges

import cv2
import numpy as np
import os
src = 'C:\\D\\DSU\\Dragomans\\two-page projection'
# dst1 = 'D:\\...Special_media_image_processing\\Dragomans\\types of pages we have\\project_to_y'
dst2 = 'C:\\D\\DSU\\Dragomans\\two-page projection'
# dst3 = 'E:\\DSU\\test samples\\edges'
dst4 = 'C:\\D\\DSU\\Dragomans\\two-page projection'

def project(name, impath, index, to_axis):
    # Load the image and preprocess it
    image = cv2.imread(impath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 120, apertureSize=3)
    height, width = edges.shape

    # create a bunch of save paths for the code that follows
    nm, ext = os.path.splitext(name)
    new_name = f"{nm}_{index}{ext}"
    new_path_x = os.path.join(dst2, new_name)
    new_path_y = os.path.join(dst4, new_name)
    # new_path_e = os.path.join(dst3, new_name)
    # cv2.imwrite(new_path_e, edges)

    projection = []
    if to_axis == 'x':
        for x in range(0, width - 1):
            projection.append(np.sum(edges[:, x]))
        npprojection = np.array(projection)
        max_val = np.max(npprojection)

        # grayscale images are 2D np arrays with max value 255, so I need to 
        # normalize the np array so thta the max value is 255
        normalized = np.floor(npprojection / max_val * 255)
        result = normalized.astype(int)
        avg = np.mean(result) * 0.7

        # the code in the for loop above created a strip of pixels
        # to make this strip easier for human analysis, I have to tile it multiple times
        h_outimage = np.tile(result, (500, 1))
        rotated = h_outimage.astype('uint8')

        # use normal thresholding and binarilization to make the projection cleaner
        ret, rotated = cv2.threshold(rotated, avg, 255, cv2.THRESH_BINARY)
        cv2.imwrite(new_path_x, rotated)
    if to_axis == 'y':
        for y in range(0, height - 1):
            projection.append(np.sum(edges[y, :]))
        npprojection = np.array(projection)
        max_val = np.max(npprojection)
        normalized = np.floor(npprojection / max_val * 255)
        result = normalized.astype(int)
        avg = np.mean(result) * 1.45
        v_outimage = np.tile(result, (500, 1))
        rotated = cv2.rotate(v_outimage, cv2.ROTATE_90_COUNTERCLOCKWISE)
        rotated = rotated.astype('uint8')
        ret, rotated = cv2.threshold(rotated, avg, 255, cv2.THRESH_BINARY)
        print('adaptive')
        cv2.imwrite(new_path_y, rotated)

i = 1
for filename in os.listdir(src):
    imgpath = os.path.join(src, filename)
    if filename.endswith(('.jpg', '.jpeg', '.JPG')):
        project(filename, imgpath, i, 'x')
        i += 1