import cv2
import numpy as np

# Load the image
image = cv2.imread('/home/adwait/myFolder/visualQuerySystem/PSData/flowchart5.png')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply binary thresholding
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

print(len(contours), contours)
# Lists to store detected modules and arrows
modules = []
arrows = []

for contour in contours:
    # Approximate the contour
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # Check if it's a rectangle (4 vertices)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        modules.append((x, y, w, h))  # Save rectangle dimensions
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw rectangle

    # If more vertices, classify as an arrow (simplified logic)
    elif len(approx) > 4:
        arrows.append(contour)
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 3)  # Draw arrow

# Display the results
cv2.imwrite("output1.png", image)
print("Image saved as output.png. Open it using any image viewer.")