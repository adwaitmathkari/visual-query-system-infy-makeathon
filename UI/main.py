from flask import Flask, request, render_template
# from py2neo import Graph
import pytesseract
from PIL import Image
import cv2
# import numpy as np
# import pytesseract

class DiagramQuestionAnsweringSystem:
    def __init__(self):
        # Initialize Flask app
        self.app = Flask(__name__)

        # Neo4j connection (replace with your instance details)
        # self.graph = Graph("neo4j+s://<your-instance-id>.databases.neo4j.io", auth=("neo4j", "<your-password>"))

        # Set up routes
        self.setup_routes()

    def setup_routes(self):
        """Set up the routes for Flask."""
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/upload', 'upload_image', self.upload_image, methods=['POST'])
        # self.app.add_url_rule('/query', 'query_database', self.query_database, methods=['POST'])

    def index(self):
        """Render the index page."""
        return render_template('index.html')

    def upload_image(self):
        """Handle image upload and OCR processing."""
        if 'image' not in request.files:
            return 'No file uploaded', 400
        file = request.files['image']
        if file.filename == '':
            return 'No selected file', 400

        # Process the uploaded image with OCR
        image = Image.open(file.stream)

        extracted_text = self.processImage(image)

        # extracted_text = pytesseract.image_to_string(image)

        # Print extracted text for debugging
        print(f"Extracted text: {extracted_text}")

        if not extracted_text.strip():  # Check if extracted text is empty
            return 'OCR failed to extract any text. Please try a clearer image.', 400

        # Save extracted text to Neo4j
        # self.graph.run("CREATE (d:Diagram {content: $content})", content=extracted_text)

        # Debug: Verify saved text in database
        # result = self.graph.run("MATCH (d:Diagram) RETURN d LIMIT 1").data()
        # print("Saved Diagram:", result)

        return f'OCR Text Saved: {extracted_text}'

    # def query_database(self):
    #     """Handle user queries about the diagrams in Neo4j."""
    #     query = request.form['query']
    #     try:
    #         result = self.graph.run(query).data()
    #         return render_template('query_result.html', result=result)
    #     except Exception as e:
    #         return f'Error: {str(e)}', 400

    def processImage(image):
        
        # Convert to grayscale
        finalImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, thresh = cv2.threshold(finalImage, 240, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Lists to store detected rectangles (nodes) and arrows (connections)
        rectangles = []
        textInRectangles = []
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
                
                textInRectangles.append(text2.strip().replace('\n', ' ').strip())


            # If contour is elongated, classify it as an arrow
            elif len(approx) > 4:
                area = cv2.contourArea(contour)
                if area > 50:  # Filter small noise
                    arrows.append(contour)
                    cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)  # Red arrows
        print(len(rectangles), len(arrows))
        # Save the output image
        output_path = 'output.png'
        cv2.imwrite(output_path, image)

        print("Detection complete. The output image with rectangles and arrows is saved as 'flowchart_detected_output.png'.")
        # Run the Flask app   
        detectedText = [f"Box {i + 1}. {value}" for i, value in enumerate(textInRectangles)]
        return detectedText
    

    def run(self):
        """Run the Flask app."""
        self.app.run(debug=True)


# Create the instance of the system and run it
if __name__ == '__main__':
    system = DiagramQuestionAnsweringSystem()
    system.run()
