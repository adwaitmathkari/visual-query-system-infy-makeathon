import cv2
import numpy as np
import pytesseract

# Load the image
image = cv2.imread('/home/adwait/myFolder/visualQuerySystem/PSData/flowchart10.png')

# Convert to grayscale
finalImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply binary thresholding
_, thresh = cv2.threshold(finalImage, 240, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Lists to store detected rectangles (nodes) and arrows (connections)
rectangles = []
arrows = []
print(len(contours))
r=1
for contour in contours:
    # Approximate the contour
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # If contour has 4 points, it's likely a rectangle (node)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        rectangles.append((x, y, w, h))
        croppedRectangle = finalImage[y:y + h, x:x + w]
        cv2.imwrite('rect'+ str(r) + '.png', croppedRectangle)
        r+=1
        # Apply OCR to extract text
        # text = pytesseract.image_to_string(croppedRectangle, config='--psm 6')  # '--psm 6' treats the ROI as a block of text
        text2 = pytesseract.image_to_string(croppedRectangle)  # '--psm 6' treats the ROI as a block of text
        
        # print('Found text inside rectangle', (x, y, w, h), ':', text)
        print('Found text inside rectangle', (x, y, w, h), ':', text2.strip().replace('\n', ' ').strip())

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangles

    # If contour is elongated, classify it as an arrow
    elif len(approx) > 4:
        area = cv2.contourArea(contour)
        if area > 50:  # Filter small noise
            arrows.append(contour)
            cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)  # Red arrows
print(len(rectangles), len(arrows), arrows)
# Save the output image
output_path = 'output.png'
cv2.imwrite(output_path, image)

print("Detection complete. The output image with rectangles and arrows is saved as 'flowchart_detected_output.png'.")
