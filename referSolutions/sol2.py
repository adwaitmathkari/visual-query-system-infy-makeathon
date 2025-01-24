import cv2
import numpy as np
import pytesseract
import networkx as nx
from collections import defaultdict
import spacy
 
# Load spaCy model for NLU
nlp = spacy.load("en_core_web_sm")
 
# Step 1: Image Preprocessing and Object Detection
def preprocess_image(image_path):
    # Load the image
    img = cv2.imread(image_path)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur and thresholding for edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
    return img, thresh

# Step 2: Detecting nodes (modules) and edges (arrows)
def detect_modules_and_connections(thresh_img):
    # Find contours (which represent modules and connections)
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours), contours)
    modules = []
    edges = []
    for contour in contours:
        # Approximate the contour to find rectangular shapes (modules)
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:  # likely to be a rectangle
            x, y, w, h = cv2.boundingRect(approx)
            modules.append((x, y, w, h))  # Store the coordinates of the module (rectangles)
        # Otherwise, check for arrows or connections (edges)
        # This part can be more sophisticated by looking for specific arrow patterns in the image
        if len(approx) > 4:
            # Assuming we can classify these as edges/arrows (simplified logic here)
            edges.append(contour)
    return modules, edges
 
# Step 3: Parse Data Flow (create relationships between modules)
def create_data_flow_graph(modules, edges):
    G = nx.DiGraph()
    for i, module in enumerate(modules):
        module_id = f"Module_{i}"
        G.add_node(module_id, coordinates=module)
    for edge in edges:
        # This would require additional logic to detect direction and flow
        # For simplicity, we'll add a direct connection between two random modules
        # (you should add actual logic for this based on your diagram's design)
        G.add_edge("Module_0", "Module_1", data_flow="Type_A")  # Example data flow
    return G
 
# Step 4: Querying via Natural Language
def process_query(query, graph):
    doc = nlp(query)
    # Here, we would process the query to identify which modules are being asked about
    # For now, let's assume we always query for the data flow between two modules
    if "data flow" in query:
        nodes = list(graph.nodes())
        data = defaultdict(list)
        for node in nodes:
            for neighbor in graph.neighbors(node):
                flow_type = graph[node][neighbor]["data_flow"]
                data[node].append((neighbor, flow_type))
        return data
 
# Main Function to Run the Process
def main(image_path, query):
    img, thresh_img = preprocess_image(image_path)
    modules, edges = detect_modules_and_connections(thresh_img)
    print(modules, edges)
    print(len(modules), len(edges))

    # data_flow_graph = create_data_flow_graph(modules, edges)
    # result = process_query(query, data_flow_graph)
    return result
 
# Example Usage
if __name__ == "__main__":
    image_path = "/home/adwait/myFolder/visualQuerySystem/PSData/flowchart5.png" 
    query = "What is the data flow between the modules?"
    result = main(image_path, query)
    print(result)







    