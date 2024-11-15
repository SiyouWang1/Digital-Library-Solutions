from skimage.transform import radon
from PIL import Image
import numpy as np
from numpy.fft import rfft
import cv2
import warnings
import shutil
import time
import os
warnings.filterwarnings("ignore")
try:
    # More accurate peak finding from
    # https://gist.github.com/endolith/255291#file-parabolic-py
    from parabolic import parabolic

    def argmax(x):
        return parabolic(x, np.argmax(x))[0]
except ImportError:
    print('import parabolic error')



src = 'E:\\DSU\\test samples'
mistake_folder = 'E:\\DSU\\test samples\\mistakes'

def rms_flat(a):
    # Return the root mean square of all the elements of *a*, flattened out.
    return np.sqrt(np.mean(np.abs(a) ** 2))


def orientation_detect(imgpath, angle_interval, line_spacing, method):
    image = cv2.imread(imgpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.Canny(gray, 50, 120, apertureSize=3)
    # Demean; make the brightness extend above and below zero
    gray = gray - np.mean(gray)  

    # do discrete Radon transform every 'angles' degree
    angles = np.arange(0, 180, angle_interval)
    angles = angles.tolist()
    sinogram = radon(gray, angles)

    # find the desired row by using FFT and find the row with the most dominant
    # frequency among a certain frequency interval
    special_rows = []
    y, x = np.shape(sinogram)
    Tsino = sinogram.transpose()
    tune_length = line_spacing * 2
    # Loop through each row of the image
    for row in enumerate(Tsino):
        # Subtract the mean to normalize the row
        normalized_row = row[1] - np.mean(row[1])
        
        # Compute the Fourier Transform of the row
        spectrum = np.abs(np.fft.fft(normalized_row)) / y
        # Focus on the desired frequencies
        spectrum = spectrum[y // tune_length : y // 3]
        
        # print(f'col {i} dominant is {peak / avg_magnitude} stronger than average')
        # find the best row by checking whether or not the peak frequency's magnitude
        # is significantly higher than the average magnitude
        if method == 'peak':
            peak = np.max(spectrum)
            avg_magnitude = np.mean(spectrum)
            special_rows.append(peak / avg_magnitude)
        
        # Find the best row by selecting the row with the frequency of maximum magnitude
        elif method == 'max':
            peak = np.max(spectrum)
            special_rows.append(peak / avg_magnitude)

        # find the best row by using variance
        elif method == 'var':
            special_rows.append(np.var(spectrum))

    # if the best row appears close the 90 degrees region, mark this image as upright
    mid = 90 // angle_interval
    left = mid - 1
    right = mid + 1
    if np.argmax(special_rows) in [left, mid, right]:
        return True
    else:
        return False

start_time = time.time()
s = 0
f = 0
i = 0
for filename in os.listdir(src):
    imgpath = os.path.join(src, filename)
    if filename.endswith(('.jpg', '.jpeg', '.JPEG', '.JPG', '.png', '.gif', '.tif')):
        i += 1
        print(f'the {i}th image')
        if orientation_detect(imgpath, 30, 45, 'peak'):
            s += 1
        else:
            f += 1
            shutil.copy(imgpath, mistake_folder)
    print(f'success rate is {s/(s+f)}')
end_time = time.time()
time_length = end_time - start_time
print(f"Time elapsed: {time_length:.6f} seconds")