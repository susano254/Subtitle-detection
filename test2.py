import cv2
import numpy as np

# Read the frame
frame = cv2.imread('frame.jpg')

# Get the height and width of the frame
height, width, _ = frame.shape

# Define the region of interest (bottom 20% of the image)
lower_part_start = int(height * (1 - 20 / 100))

# Extract the bottom 20% of the frame
roi = frame[lower_part_start:, :]

# Convert to grayscale
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

kernel_size = 7
# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

# Perform Canny edge detection
edges = cv2.Canny(blurred, 50, 100)
cv2.imshow('Canny Edges', edges)
cv2.waitKey(0)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on a copy of the frame
contour_frame = roi.copy()
cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 2)
cv2.imshow('Contours', contour_frame)
cv2.waitKey(0)

rectangles = []
for contour in contours:
    # Filter contours based on area
    x, y, w, h = cv2.boundingRect(contour)
    rectangles.append((cv2.boundingRect(contour)))
    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 200, 0), 1)

# Display the result
cv2.imshow('Subtitle Detection', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()