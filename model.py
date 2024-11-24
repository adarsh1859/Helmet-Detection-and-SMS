import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

class YOLOv3HelmetDetector:
    def __init__(self, weights_path, config_path, names_path, input_size=416):
        self.net = cv2.dnn.readNet(weights_path, config_path)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.classes = self.load_classes(names_path)
        self.input_size = input_size

    def load_classes(self, names_path):
        with open(names_path, 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        return classes

    def detect(self, image):
        height, width, channels = image.shape
        blob = cv2.dnn.blobFromImage(image, 0.00392, (self.input_size, self.input_size), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        results = []
        for i in indices:
            i = i[0]
            box = boxes[i]
            x, y, w, h = box
            results.append((x, y, x + w, y + h, confidences[i], class_ids[i]))
        return results

# Instantiate the detector
weights_path = 'yolov3.weights'
config_path = 'yolov3.cfg'
names_path = 'coco.names'
helmet_detector = YOLOv3HelmetDetector(weights_path, config_path, names_path)
