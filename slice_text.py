# This python script is used to crop the image into windows of 384*384
# pieces. If the width or height of the image is not a multiple of 384,
# then the last image slice in that row or column will overlap partly 
# with the second-to-last slice

# Why writing this script? This script is used to pre-process images
# with texts so that they can be fed into the CNN model for more
# emphasis on the letters. After all, what best characterizes the 
# orientation of images are the letters.

import time
import numpy as np
import cv2
import shutil
import os


src = 'C:\\D\\DSU\\Kanagaratnam\\test_rotation\\76_sample'


def select_text(width, height, impath, ith):
    image = cv2.imread(impath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.GaussianBlur(gray, (11, 11), 7)
    canny = cv2.Canny(img_blurred, 90, 150, apertureSize=3)
    h, w = np.shape(gray)
    remainder_h, remainder_w = h%height, w%width
    if remainder_h == 0:
        chunk_count_h = h//height
    else:
        chunk_count_h = h//height+1
    if remainder_w == 0:
        chunk_count_w = w//width
    else:
        chunk_count_w = w//width+1
    chunk_offset_h, chunk_offset_w = height-remainder_h//chunk_count_h-1, width-remainder_w//chunk_count_w-1

    slices = []
    y = 0
    while y + height - 1 <= h:
        x = 0
        while x + width - 1 <= w:
            slices.append(canny[y:y+chunk_offset_h, x:x+chunk_offset_w])
            x += chunk_offset_w
        y += chunk_offset_h
    
    img_edge_pairs = []
    for imgslice in slices:
        edge_count = np.count_nonzero(imgslice == 255)
        img_edge_pairs.append((imgslice, edge_count))
    sorted_slices = sorted(img_edge_pairs, key=lambda x:x[1])
    return sorted_slices[-ith][0]


start_time = time.time()
i = 0
for filename in os.listdir(src):
    imgpath = os.path.join(src, filename)
    print(f'{i}th image')
    i += 1
    nm, ext = os.path.splitext(filename)
    if filename.endswith(('.jpg', '.jpeg', '.JPEG', '.JPG', '.png', '.gif', '.tif', '.TIF')):
        cv2.imwrite(os.path.join(src, nm+'text'+ext), select_text(384, 384, imgpath, 1))
end_time = time.time()
time_length = end_time - start_time
print(f"Time elapsed: {time_length:.6f} seconds")