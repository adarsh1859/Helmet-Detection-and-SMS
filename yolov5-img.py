import torch
import torchvision.transforms as transforms
import cv2
import numpy as np

# Load pre-trained YOLOv5 model from PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Load the video
video_path = 'VID20240312143027.mp4'
cap = cv2.VideoCapture(video_path)

# Check if video capture was successful
if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

# Get the original video size
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the desired window size
window_width = 800  # You can adjust this value according to your preference

# Check if frame width is 0 to avoid division by zero
if frame_width == 0:
    print("Error: Frame width is zero.")
    exit()

# Calculate the scale factor for resizing the frames
scale_factor = window_width / frame_width

# Define a list of class names for YOLOv5s
class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 
               'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 
               'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 
               'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 
               'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 
               'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 
               'hair drier', 'toothbrush']

# Perform object detection on each frame of the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame while maintaining the aspect ratio
    frame_resized = cv2.resize(frame, (window_width, int(frame_height * scale_factor)))

    # Perform object detection on the resized frame
    results = model(frame_resized)

    # Draw bounding boxes and labels
    for detection in results.pred[0]:
        class_id = detection[-1]
        score = detection[-2].item()
        label = class_names[int(class_id)]
        bbox = detection[:4].tolist()
        bbox = [int(coord) for coord in bbox]

        # Scale the bounding box coordinates back to the original frame size
        bbox_scaled = [int(coord / scale_factor) for coord in bbox]

        # Draw bounding box
        cv2.rectangle(frame, (bbox_scaled[0], bbox_scaled[1]), (bbox_scaled[2], bbox_scaled[3]), (0, 255, 0), 2)

        # Add label and confidence score
        cv2.putText(frame, f'{label}: {score:.2f}', (bbox_scaled[0], bbox_scaled[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with bounding boxes
    cv2.imshow('YOLOv5 Object Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
