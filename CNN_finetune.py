from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.models import load_model
import os
import cv2  # Import OpenCV for image processing
from PIL import ImageFile
import numpy as np
import tensorflow as tf

# Ensure GPU memory growth
gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)

# Allow loading truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Define directories for upright and upside-down images
base_dir = 'C:\\D\\DSU\\Kanagaratnam\\test_rotation\\Corrected\\train'
model_path = '11_32_512_512_canny_Tamil_and_English_finetuned.h5'
train_dir = os.path.join(base_dir)

# Load the pre-trained model
model = load_model(model_path)

# Image parameters
IMAGE_SIZE = (512, 512)  # Resize images
BATCH_SIZE = 32  # Number of images to process in one batch

# Function to apply grayscale conversion and Canny edge detection
def preprocess_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = gray_image.astype(np.uint8)  # Convert to uint8 if necessary
    edges = cv2.Canny(gray_image, 50, 120, apertureSize=3)
    edges_normalized = edges / 255.0
    return np.expand_dims(edges_normalized, axis=-1)

# Custom generator to apply the preprocessing
def custom_preprocessing_generator(generator):
    while True:
        try:
            batch_x, batch_y = next(generator)
            batch_x_processed = np.array([preprocess_image(x) for x in batch_x])
            yield batch_x_processed, batch_y
        except OSError as e:
            print(f"Error loading image, skipping batch: {e}")

# Data augmentation and basic preprocessing with ImageDataGenerator
datagen = ImageDataGenerator(
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2  # 80% train, 20% validation split
)

# Create training and validation datasets
train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    train_dir,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation'
)

# Create custom generators that include the preprocessing
train_preprocessed = custom_preprocessing_generator(train_generator)
validation_preprocessed = custom_preprocessing_generator(validation_generator)

# Print model summary
model.summary()

# Compile the loaded model if needed (not strictly required if already compiled)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Continue training the model using the custom preprocessed generator
history = model.fit(
    train_preprocessed,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=8,
    validation_data=validation_preprocessed,
    validation_steps=validation_generator.samples // BATCH_SIZE
)

# Save the updated model for future use
model.save('11_32_512_512_canny_Tamil_and_English_finetuned2.h5')