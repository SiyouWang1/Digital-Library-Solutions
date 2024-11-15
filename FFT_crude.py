import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load and preprocess the image
image = cv2.imread('image_path.jpg', cv2.IMREAD_GRAYSCALE)

# List to store indices of special rows; 
# the meaning of'special' depends on the code that follows
special_rows = []

# Define a threshold to identify the dominant frequency
threshold_ratio = 0.5  # This can be adjusted based on the specific pattern

# Loop through each row of the image
for i, row in enumerate(image):
    # Subtract the mean to normalize the row
    normalized_row = row - np.mean(row)
    
    # Compute the Fourier Transform of the row
    spectrum = np.abs(np.fft.fft(normalized_row))
    
    # Focus on the positive frequencies
    spectrum = spectrum[:len(spectrum) // 2]
    
    # Identify the maximum peak in the spectrum
    peak = np.max(spectrum)
    
    # Compute the average magnitude of the spectrum
    avg_magnitude = np.mean(spectrum)
    
    # Check if the peak is significantly higher than the average magnitude
    if peak > threshold_ratio * avg_magnitude:
        special_rows.append(i)

# Display the special rows
print(f"Special rows with regular pattern: {special_rows}")

# Optionally, visualize the detected special rows
for row_index in special_rows:
    plt.plot(image[row_index], label=f"Row {row_index}")
plt.legend()
plt.title("Detected Special Rows")
plt.show()
