import cv2
import numpy as np
import imutils

from Helper import Helper


# tuplify
def tup(point):
    return (point[0], point[1]);

# returns true if the two boxes overlap
def overlap(source, target):
    # unpack points
    tl1, br1 = source;
    tl2, br2 = target;

    # checks
    if (tl1[0] >= br2[0] or tl2[0] >= br1[0]):
        return False;
    if (tl1[1] >= br2[1] or tl2[1] >= br1[1]):
        return False;
    return True;

# returns all overlapping boxes
def getAllOverlaps(boxes, bounds, index):
    overlaps = [];
    for a in range(len(boxes)):
        if a != index:
            if overlap(bounds, boxes[a]):
                overlaps.append(a);
    return overlaps;

# Read the frame
frame = cv2.imread('frame.jpg')
orig = np.copy(frame)


# Get the height and width of the frame
height, width, _ = frame.shape
lower_part_start = int(height * (1 - 20 / 100))

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

# go through the contours and save the box edges
boxes = [] # each element is [[top-left], [bottom-right]];
hierarchy = hierarchy[0]
for component in zip(contours, hierarchy):
    currentContour = component[0]
    currentHierarchy = component[1]
    x,y,w,h = cv2.boundingRect(currentContour)
    if currentHierarchy[3] < 0:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
        boxes.append([[x,y], [x+w, y+h]]);



def merge_boxes(rectangles, merge_margin_x=10, merge_margin_y=1):
    boxes = rectangles.copy()

    finished = False;
    highlight = [[0,0], [1,1]];
    points = [[[0,0]]];
    while not finished:
        # set end con
        finished = True;

        # loop through boxes
        index = 0;
        while index < len(boxes):
            # grab current box
            curr = boxes[index];

            # add margin
            tl = curr[0][:];
            br = curr[1][:];
            tl[0] -= merge_margin_x;
            tl[1] -= merge_margin_y;
            br[0] += merge_margin_x;
            br[1] += merge_margin_y;

            # get matching boxes
            overlaps = getAllOverlaps(boxes, [tl, br], index);
            
            # check if empty
            if len(overlaps) > 0:
                # combine boxes
                # convert to a contour
                con = [];
                overlaps.append(index);
                for ind in overlaps:
                    tl, br = boxes[ind];
                    con.append([tl]);
                    con.append([br]);
                con = np.array(con);

                # get bounding rect
                x,y,w,h = cv2.boundingRect(con)

                # stop growing
                w -= 1
                h -= 1
                merged = [[x,y], [x+w, y+h]]

                # highlights
                highlight = merged[:]
                points = con

                # remove boxes from list
                overlaps.sort(reverse = True);
                for ind in overlaps:
                    del boxes[ind]
                boxes.append(merged)

                # set flag
                finished = False;
                break

            # increment
            index += 1
    return boxes

word_boxes = merge_boxes(boxes)
line_boxes = merge_boxes(word_boxes, merge_margin_x=10, merge_margin_y=0)

# show final
copy = np.copy(orig);


for box in line_boxes:
    cv2.rectangle(copy, tup(box[0]), tup(box[1]), (0,200,0), 1);
cv2.imshow("Final", copy);
cv2.waitKey(0);