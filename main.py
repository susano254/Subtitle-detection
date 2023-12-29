import cv2
import numpy as np

from Helper import Helper


# Read the frame
frame = cv2.imread('frame.jpg')

# Get the height and width of the frame
height, width, _ = frame.shape

# Define the region of interest (bottom 20% of the image)
lower_part_start = int(height * (1 - 20 / 100))
# Extract the bottom 20% of the frame
roi = frame[lower_part_start:, :]


# Convert to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

kernel_size = 7
# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

# Perform Canny edge detection
edges = cv2.Canny(blurred, 50, 100)
cv2.imshow('Canny Edges', edges)
cv2.waitKey(0)

# Find contours
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
hierarchy = hierarchy[0]

# Draw contours on a copy of the frame
contour_frame = frame.copy()
cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 2)
cv2.imshow('Contours', contour_frame)
cv2.waitKey(0)

rectangles = [] 
for component in zip(contours, hierarchy):
    currentContour = component[0]
    currentHierarchy = component[1]
    x,y,w,h = cv2.boundingRect(currentContour)

    if currentHierarchy[3] < 0:
        rectangles.append((x, y, x+w, y+h));

finished = False
merged = False
while not finished:
    finished = True
    for i in range(len(rectangles)):
        if merged:
            break
        for j in range(len(rectangles)):
            if i == j:
                continue

            merged = False
            if Helper.rectangles_overlap(rectangles[i], rectangles[j]):
                temp = []
                x1, y1, w1, h1 = rectangles[i]
                x2, y2, w2, h2 = rectangles[j]

                temp.append([x1, y1])
                temp.append([x1+w1, y1+h1])
                temp.append([x2, y2])
                temp.append([x2+w2, y2+h2])
                temp = np.array(temp)

                merged_rect = cv2.boundingRect(temp)

                if(i > j):
                    rectangles.remove(rectangles[i])
                    rectangles.remove(rectangles[j])
                else:
                    rectangles.remove(rectangles[j])
                    rectangles.remove(rectangles[i])

                rectangles.append(merged_rect)
                merged = True
                finished = False
                break

for rect in rectangles:
    x,y,w,h = rect
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,200,0), 1);




# Display the result
cv2.imshow('Subtitle Detection', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()