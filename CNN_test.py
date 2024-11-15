from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os
import cv2  # Import OpenCV for image processing
from PIL import ImageFile
import numpy as np
import scipy
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)

# Allow loading truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Define directories for upright and upside-down images
base_dir = 'C:\\D\\DSU\\Kanagaratnam\\test_rotation\\Generated Tamil Pages'
train_dir = os.path.join(base_dir)

# Image parameters
IMAGE_SIZE = (512, 512)  # Resize images
BATCH_SIZE = 32  # Number of images to process in one batch

# Function to apply grayscale conversion and Canny edge detection
def preprocess_image(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = gray_image.astype(np.uint8)  # Convert to uint8 if necessary
    # Apply Canny edge detection
    edges = cv2.Canny(gray_image, 50, 120, apertureSize=3)
    
    # Normalize the image (important since we're dividing by 255 later in rescale)
    edges_normalized = edges / 255.0
    
    # Expand dimensions to make it compatible with CNN input
    return np.expand_dims(edges_normalized, axis=-1)  # Add channel dimension

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
    shear_range=0.1,
    zoom_range=0.1,
    validation_split=0.1  # 80% train, 20% validation split
)

# Create training and validation datasets
train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',  # Binary classification: upright or upsidedown
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

# Build the CNN model
model = models.Sequential([
    # First convolution layer with pooling
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(512, 512, 1)),  # Note: input shape change
    layers.MaxPooling2D(2, 2),

    # Second convolution layer with pooling
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    # Third convolution layer with pooling
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    # Add another pooling layer to reduce size further
    layers.MaxPooling2D(2, 2),  # Reducing spatial dimensions more for larger input size

    # Flatten and fully connected layers
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # Binary output: 0 (upsidedown) or 1 (upright)
])

# Print model summary to inspect layer sizes
model.summary()

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model using the custom preprocessed generator
history = model.fit(
    train_preprocessed,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=11,  # Adjust number of epochs as needed
    validation_data=validation_preprocessed,
    validation_steps=validation_generator.samples // BATCH_SIZE
)

# Save the model for future use
model.save('11_32_512_512_canny_Tamil_and_English_artificial_and_tagged_training.h5')