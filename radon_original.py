"""
Automatically detect rotation and line spacing of an image of text using
Radon transform
If image is rotated by the inverse of the output, the lines will be
horizontal (though they may be upside-down depending on the original image)
It doesn't work with black borders
"""

from skimage.transform import radon
from PIL import Image
from numpy import asarray, mean, array, blackman
import numpy as np
from numpy.fft import rfft
import matplotlib.pyplot as plt
import cv2
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


def rms_flat(a):
    # Return the root mean square of all the elements of *a*, flattened out.
    return np.sqrt(np.mean(np.abs(a) ** 2))


imgpath = '05295!!!Senato Del. Filze 15 - IMG_0113.JPG'
image = cv2.imread(imgpath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.Canny(gray, 50, 120, apertureSize=3)
# Demean; make the brightness extend above and below zero
# gray = gray - mean(gray)  
gray = gray - mean(gray)  # Demean; make the brightness extend above and below zero
plt.subplot(2, 2, 1)
plt.imshow(gray)

angle_interval = 1
angles = np.arange(0, 180, angle_interval)
angles = angles.tolist()
# Do the radon transform and display the result
sinogram = radon(gray, angles)

plt.subplot(2, 2, 2)
plt.imshow(sinogram.T, aspect='auto')
plt.gray()

# Find the RMS value of each row and find "busiest" rotation,
# where the transform is lined up perfectly with the alternating dark
# text and white lines
r = array([rms_flat(line) for line in sinogram.transpose()])
rotation = (argmax(r)) * angle_interval
print('Rotation: {:.2f} degrees'.format(90 - rotation))
plt.axhline(rotation, color='r')

# Plot the busy row
row = sinogram[:, rotation]
N = len(row)
plt.subplot(2, 2, 3)
plt.plot(row)

# Take spectrum of busy row and find line spacing
window = blackman(N)
spectrum = rfft(row * window)
plt.plot(row * window)
frequency = argmax(abs(spectrum))
line_spacing = N / frequency  # pixels
print('Line spacing: {:.2f} pixels'.format(line_spacing))

plt.subplot(2, 2, 4)
plt.plot(abs(spectrum))
plt.axvline(frequency, color='r')
plt.yscale('log')
plt.show()