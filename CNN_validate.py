# Load and preprocess a new image for prediction
import tensorflow as tf
from PIL import ImageFile
import shutil
import cv2
import os

# the first (128*128) and second model (300*300) used RGB without pre-processing,
# while the third (400*400) used grayscale and canny edge detection. Hence, the
# shapes are [1, 128, 128, 3], [1, 300, 300, 3], and [1, 400, 400, 1]

# Load the model for future predictions
model = tf.keras.models.load_model('orientation_classifier.h5')

# Set up basic parameters
folder_path = 'C:\\D\\DSU\\Dragomans\\upright - Copy\\upside-down'
mistake_path1 = 'C:\\D\\DSU\\Dragomans\\upright - Copy\\upside-down mistakes'
mistake_path2 = 'C:\\D\\DSU\\Dragomans\\upright - Copy\\upright mistakes'
IMAGE_SIZE = (128, 128)

def get_img_orientation(image_path):
    image_gray = cv2.imread(image_path)
    
    # Convert to grayscale (1 channel instead of 3)
    # image_gray = cv2.cvtColor(image_gray, cv2.COLOR_BGR2GRAY)
    image_resized = cv2.resize(image_gray, IMAGE_SIZE)
    # image_resized = cv2.Canny(image_resized, threshold1=50, threshold2=120)
    edges_normalized = image_resized / 255.0
    edges_reshaped = edges_normalized.reshape(1, 128, 128, 3)  # Add batch and channel dimensions

    return model.predict(edges_reshaped)


up = 0
down = 0
i = 0
for filename in os.listdir(folder_path):
    imgpath = os.path.join(folder_path, filename)
    if filename.endswith(('.jpg', '.jpeg', '.JPEG', '.JPG', '.png', '.gif', '.TIF')):
        i += 1
        print(f'the {i}th image')
        try:
            # Attempt to process the image
            result = get_img_orientation(imgpath)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue  # Skip to the next file
        print(result[0])
        if result[0] <= 0.5: #value smaller or equal to 0.5 means up
            up += 1
            # Use this copy command if I'm dealing with upside-down dataset
            shutil.copy2(imgpath, mistake_path1)
        else:
            down += 1
            # Use this copy command if I'm dealing with upright dataset
            # shutil.copy2(imgpath, mistake_path2)
    print(f'percentage of upright images is {(up / (up + down)) * 100}%')