import cv2
import numpy as np
import os
import time

def process_with_east(input_image_path, output_image_path, scale_down):
    # Load the image
    image = cv2.imread(input_image_path)
    if image is None:
        print(f"Error: Unable to load image at {input_image_path}")
        return
    
    orig = image.copy()
    (H, W) = image.shape[:2]

    # EAST requires the input size to be multiples of 32
    (newW, newH) = (W // (32*scale_down) * 32, H // (32*scale_down) * 32)
    rW = W / float(newW)
    rH = H / float(newH)
    blur = cv2.GaussianBlur(image, (9, 9), 7)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    resized_image = cv2.resize(otsu, (newW, newH))
    color = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2BGR)
    cv2.imwrite('output.png', color)

    # Load the pre-trained EAST text detector
    net = cv2.dnn.readNet(r"C:\\Users\\user\\Downloads\\frozen_east_text_detection.pb")

    # Prepare the image for the EAST model
    blob = cv2.dnn.blobFromImage(color, 1.0, (newW, newH),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)

    # Get the output layer names
    output_layers = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
    (scores, geometry) = net.forward(output_layers)

    # Decode the predictions to find bounding boxes
    def decode_predictions(scores, geometry):
        (num_rows, num_cols) = scores.shape[2:4]
        rects = []
        confidences = []

        for y in range(num_rows):
            for x in range(num_cols):
                score = scores[0, 0, y, x]
                if score < 0.5:  # Confidence threshold
                    continue

                # Extract the bounding box coordinates
                offsetX, offsetY = x * 4.0, y * 4.0
                angle = geometry[0, 4, y, x]
                cos = np.cos(angle)
                sin = np.sin(angle)
                h = geometry[0, 0, y, x]
                w = geometry[0, 1, y, x]

                endX = int(offsetX + (cos * w) + (sin * h))
                endY = int(offsetY - (sin * w) + (cos * h))
                startX = int(offsetX - (cos * w) - (sin * h))
                startY = int(offsetY + (sin * w) - (cos * h))

                rects.append((startX, startY, endX, endY))
                confidences.append(float(score))

        return (rects, confidences)

    (rects, confidences) = decode_predictions(scores, geometry)

    # Apply Non-Maximum Suppression to suppress overlapping boxes
    boxes = cv2.dnn.NMSBoxes(rects, confidences, 0.5, 0.4)

    # Draw bounding boxes on the original image
    if len(boxes) > 0:
        for i in boxes.flatten():
            (startX, startY, endX, endY) = rects[i]
            # Scale back to the original image size
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)

            # Draw the bounding box
            cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Save the output image as a PNG file
    cv2.imwrite(output_image_path, orig)
    print(f"Processed image saved as: {output_image_path}")

# Example usage
input_image = "0000013.tif"  # Replace with the path to your .tif image
output_image = "output_image.png"  # Replace with the desired path for the .png image

start_time = time.time()
process_with_east(input_image, output_image, 8)
end_time = time.time()
time_length = end_time - start_time
print(f"Time elapsed: {time_length:.6f} seconds")