import cv2
import numpy as np

# Load an image
image_path = 'shre-image.jpeg'
image = cv2.imread(image_path)

# Check if the image is loaded successfully
if image is None:
    print('Error: Unable to load image')
else:
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Detect edges using Canny edge detection
    edges = cv2.Canny(blurred_image, 50, 150)

    # Resize all images to a common size
    size = (200, 200)
    resized_image = cv2.resize(image, size)
    resized_gray_image = cv2.resize(gray_image, size)
    resized_blurred_image = cv2.resize(blurred_image, size)
    resized_edges = cv2.resize(edges, size)

    # Convert grayscale images to 3-channel images
    resized_gray_image = cv2.cvtColor(resized_gray_image, cv2.COLOR_GRAY2BGR)
    resized_blurred_image = cv2.cvtColor(resized_blurred_image, cv2.COLOR_GRAY2BGR)

    # Convert edges to 3-channel image
    resized_edges = cv2.cvtColor(resized_edges, cv2.COLOR_GRAY2BGR)

    # Create a square canvas to display all images
    canvas_size = (2*size[0], 2*size[1])
    canvas = 255 * np.ones((canvas_size[1], canvas_size[0], 3), dtype=np.uint8)

    # Arrange images on the canvas
    canvas[0:size[1], 0:size[0]] = resized_image
    canvas[0:size[1], size[0]:] = resized_gray_image
    canvas[size[1]:, 0:size[0]] = resized_blurred_image
    canvas[size[1]:, size[0]:] = resized_edges

    # Display the canvas with all images
    cv2.imshow('Images', canvas)
    cv2.waitKey(0)

    # Close OpenCV window
    cv2.destroyAllWindows()
