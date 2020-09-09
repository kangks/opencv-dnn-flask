import cv2
import os
import warnings
import logging
import numpy as np

from .prediction_dto import PredictionDto

import configparser
from datetime import datetime

class ObjectDetector(object):

    file_folder = os.path.dirname(os.path.abspath(__file__))

    model_config = os.path.join(file_folder, "models/yolov4.cfg")
    weight_file = os.path.join(file_folder, "models/yolov4.weights")
    class_files = os.path.join(file_folder, "models/class.names")

    confidenceThreshold = 0.1

    scaleFactor = 1/32

    logger = logging.getLogger(__name__)

    def __init__(self):

        with open(self.class_files, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

        self.net = cv2.dnn.readNet(self.model_config, self.weight_file)

        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        config = configparser.ConfigParser(strict=False)
        config.read(self.model_config)

        self.net_inputWidth = 32 * 20
        self.net_inputHeight = self.net_inputWidth #1056 #2080

    def getOutputsNames(self, net):
        # Get the names of all the layers in the network
        layersNames = self.net.getLayerNames()
        return [layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def forward(self, frame):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        blob = cv2.dnn.blobFromImage(frame, self.scaleFactor, size=(self.net_inputWidth, self.net_inputHeight), swapRB=True, crop=False)
        self.logger.debug("blob: shape {}".format(blob.shape))

        self.net.setInput(blob)
        outs = self.net.forward(self.getOutputsNames(self.net))

        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confidenceThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = center_x - width / 2
                    top = center_y - height / 2
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])        

        # apply non-max suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidenceThreshold, 0.1)
        predictions = []
        for i in indices:
            i   = i[0]
            box = boxes[i]
            x   = box[0]
            y   = box[1]
            w   = box[2]
            h   = box[3]
            prediction = PredictionDto(x, y, w, h, self.classes[classIds[i]], classIds[i], confidences[i])
            predictions.append(prediction)

        return predictions

    def draw_boxes(self, frame, predictions, imageFactor):

        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        labelFontScale = frameHeight * 0.001

        for prediction in predictions:
            left = int( prediction.box.x / imageFactor )
            top = int( prediction.box.y / imageFactor )
            right = int( (left + prediction.box.w) / imageFactor )
            bottom = int( (top + prediction.box.h) / imageFactor )

            COLORS = (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255))

            # Draw a bounding box.
            cv2.rectangle(frame, (left, top), (right, bottom), COLORS, 3)
            
            label = "{}:{}%".format(prediction.label, int(prediction.score * 100))

            #Display the label at the top of the bounding box
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, labelFontScale, 1)
            top = max(top, labelSize[1])
            cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, labelFontScale, COLORS, 2)


        label = datetime.now().strftime("%Y%m%d-%H%M%S")
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, labelFontScale, 1)
        top = frameHeight - labelSize[1]

        cv2.putText(frame, label, (10, top), cv2.FONT_HERSHEY_SIMPLEX, labelFontScale, (255,255,255), 2)

        return frame


