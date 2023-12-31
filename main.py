import cv2
import numpy as np

from Helper import Helper


def write_video():
	# Load the video
	video = cv2.VideoCapture('Project Video.mp4')

	# Obtain video properties for output
	frame_width = int(video.get(3))
	frame_height = int(video.get(4))

	# Initialize VideoWriter
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	out = cv2.VideoWriter('output_video.mp4', fourcc, 20.0, (frame_width, frame_height))

	while True:
		ret, frame = video.read()
		if not ret:
			break

		subtitle_detect(frame)

		# Write the processed frame to the output video
		out.write(frame)

	# Release resources
	video.release()
	out.release()
	cv2.destroyAllWindows()




def subtitle_detect(frame):
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
    # Display the result
    cv2.imshow('blurred', blurred)
    cv2.waitKey(0)

    # Apply Laplacian of Gaussian (LoG)
    log_result = cv2.Laplacian(blurred, cv2.CV_64F, ksize=5)
    log_result = np.uint8(np.absolute(log_result))
    # Apply threshold to emphasize zero-crossings
    _, edges = cv2.threshold(log_result, 30, 50, cv2.THRESH_BINARY)

    # Display the result
    cv2.imshow('edges', edges)
    cv2.waitKey(0)


    k  = 3
    kernel = np.ones((k, k), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    cv2.imshow('dilated', dilated)
    cv2.waitKey(0)
    k  = 7
    kernel = np.ones((k, k), np.uint8)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    cv2.imshow('eroded', eroded)
    cv2.waitKey(0)

    edges = eroded

    # Find contours
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]

    # Draw contours on a copy of the frame
    contour_frame = roi.copy()
    copy_frame = roi.copy()
    cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 1)
    cv2.imshow('Contours', contour_frame)
    cv2.waitKey(0)

    rectangles = [] 
    for component in zip(contours, hierarchy):
        currentContour = component[0]
        currentHierarchy = component[1]

        if currentHierarchy[3] < 0:
            x,y,w,h = cv2.boundingRect(currentContour)
            rectangles.append(cv2.boundingRect(currentContour));
            cv2.rectangle(copy_frame, (x+1, y+1), (x+w-1, y+h-1), (0,250,0), 1);
    cv2.imshow('Contours', copy_frame)
    cv2.waitKey(0)
    rectangles = sorted(rectangles, key=lambda x: x[0])
    print(rectangles)
    exit()


# Read the frame
frame = cv2.imread('frame2.jpg')

subtitle_detect(frame)

# Display the result
cv2.imshow('Subtitle Detection', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()



