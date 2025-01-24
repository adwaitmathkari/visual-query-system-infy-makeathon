import cv2
import numpy as np

def detect_shapes(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Edge detection
    edges = cv2.Canny(blurred, 50, 150)
    print(edges)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)
    
    for contour in contours:
        # Approximate the contour
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Identify the shape based on the number of vertices
        x, y, w, h = cv2.boundingRect(approx)
        if len(approx) == 3:
            shape_name = "Triangle"
        elif len(approx) == 4:
            aspect_ratio = w / float(h)
            if 0.95 <= aspect_ratio <= 1.05:
                shape_name = "Square"
            else:
                shape_name = "Rectangle"
        elif len(approx) > 4:
            shape_name = "Circle"
        else:
            shape_name = "Unknown"
        print(shape_name)
        # Draw the contours and label the shape
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
        cv2.putText(image, shape_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    

    # Display the results
    # cv2.imshow("Shapes", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Path to the input image
image_path = "/home/adwait/myFolder/visualQuerySystem/PSData/basic-flowchart1.png" # Replace with your image path
detect_shapes(image_path)