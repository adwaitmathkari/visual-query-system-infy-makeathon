import cv2
import pytesseract
import networkx as nx

# Load the image
image = cv2.imread('/mnt/data/high_contrast_image.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Preprocess the image
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
edges = cv2.Canny(binary, 50, 150)

# Find contours for nodes
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
nodes = []
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    x, y, w, h = cv2.boundingRect(approx)
    if 50 < w < 200 and 20 < h < 100:  # Filter based on shape size
        nodes.append((x, y, w, h))
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Extract text from nodes
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update for your system
node_texts = {}
for (x, y, w, h) in nodes:
    roi = gray[y:y + h, x:x + w]
    text = pytesseract.image_to_string(roi, config='--psm 6').strip()
    node_texts[(x, y, w, h)] = text

# Detect arrows
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=5)
arrows = []
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        arrows.append(((x1, y1), (x2, y2)))
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

# Associate arrows with nodes
graph = nx.DiGraph()
for start, end in arrows:
    src = next((node for node in nodes if node_contains(node, start)), None)
    dest = next((node for node in nodes if node_contains(node, end)), None)
    if src and dest:
        graph.add_edge(node_texts[src], node_texts[dest])

# Visualize or save results
cv2.imshow('Processed Image', image)
cv2.waitKey(0)

# Save the graph structure
nx.write_adjlist(graph, 'flowchart_graph.adjlist')

# Helper function to check if a point is in a node
def node_contains(node, point):
    x, y, w, h = node
    px, py = point
    return x <= px <= x + w and y <= py <= y + h
