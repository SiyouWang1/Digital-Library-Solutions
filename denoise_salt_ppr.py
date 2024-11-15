import cv2
import numpy as np
import time

img_dspl_height = 3000
img_noisy = cv2.imread('0000197.TIF', 0)
x, y = np.shape(img_noisy)
# img_median = cv2.blur(img_noisy, (30, 30))
start_time = time.time()
img_median = cv2.GaussianBlur(img_noisy, (7, 7), 7)
#img_median = cv2.bilateralFilter(img_noisy, d=20, sigmaColor=40, sigmaSpace=75)
end_time = time.time()
print(f'{(end_time - start_time):.6f}')
# img_median = cv2.bilateralFilter(img_noisy, d=30, sigmaColor=40, sigmaSpace=75)
canny = cv2.Canny(img_median, 90, 150, apertureSize=3)
_, otsu = cv2.threshold(img_median, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
img_median = cv2.resize(img_median, (int(img_dspl_height / x * y), img_dspl_height))
canny = cv2.resize(canny, (int(img_dspl_height / x * y), img_dspl_height))
otsu = cv2.resize(otsu, (int(img_dspl_height / x * y), img_dspl_height))
cv2.imshow("Denoise", img_median)
cv2.imshow("Canny", canny)
cv2.imshow("otsu", otsu)
cv2.waitKey(0)
cv2.destroyAllWindows()