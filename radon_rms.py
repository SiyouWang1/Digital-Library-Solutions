import cv2
from skimage.transform import radon
from PIL import Image
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")
try:
    # More accurate peak finding from
    # https://gist.github.com/endolith/255291#file-parabolic-py
    from parabolic import parabolic

    def argmax(x):
        return parabolic(x, np.argmax(x))[0]
except ImportError:
    from numpy import argmax
src = 'D:\\...Special_media_image_processing\\Dragomans\\vertical images'


def rms_flat(a):
    # Return the root mean square of all the elements of *a*, flattened out.
    return np.sqrt(np.mean(np.abs(a) ** 2))

def orientation_detect(imgpath):
    # pre process the image
    image = cv2.imread(imgpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.Canny(gray, 50, 120, apertureSize=3)
    # below: demean; make the brightness extend above and below zero
    # gray = gray - mean(gray)  

    # integrate in the radon transform every how many degrees
    angle_interval = 2
    angles = np.arange(0, 180, angle_interval)
    angles = angles.tolist()
    sinogram = radon(gray, angles)

    # Find the RMS value of each row and find "busiest" rotation,
    # where the transform is lined up perfectly with the alternating dark
    # text and white lines
    r = np.array([rms_flat(line) for line in sinogram.transpose()])

    # True means the image is rotated 90 degrees (counter)clockwise
    rotation = (argmax(r)) * angle_interval
    print(rotation)
    if -45 < rotation < 45:
        return True
    else:
        return False
        # print('Rotation: {:.2f} degrees'.format(90 - rotation))

# apply the function to all images in a folder
s = 0
f = 0
i = 0
for filename in os.listdir(src):
    imgpath = os.path.join(src, filename)
    if filename.endswith(('.jpg', '.jpeg', '.JPG')):
        i += 1
        print(f'the {i}th image')
        if orientation_detect(imgpath):
            s += 1
        else:
            f += 1
    print(f'success rate is {s/(s+f)}')