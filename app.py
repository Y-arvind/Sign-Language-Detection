import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

folder = "Data/Z"
counter = 0
labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

while True :
    success, img = cap.read()
    imgOut = img.copy()
    hands, img = detector.findHands(img)
    if hands :
        hand = hands[0]
        x,y,w,h = hand['bbox']
        imgWhite =np.ones((imgSize, imgSize,3), np.uint8)*255
        imgCrop = img[y-offset:y+h+offset,x-offset:x+w+offset]
        imgCropShape = imgCrop.shape
        aspectRatio = h/w
        if aspectRatio>1:
            k = imgSize/h
            wCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop,(wCal , imgSize))
            imgResizeShape=imgResize.shape
            wGap = math.ceil((300-wCal)/2)
            imgWhite[:, wGap:wGap+wCal] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction,index)
        else:
            k = imgSize/w
            hCal = math.ceil(k*h)
            imgResize=cv2.resize(imgCrop,(imgSize,hCal))
            imgResizeShape=imgResize.shape
            hGap = math.ceil((300-hCal)/2)
            imgWhite[hGap:hGap+hCal,:]=imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
        cv2.rectangle(imgOut, (x-offset, y-offset-50), (x - offset +90, y-offset+50),(255,0,255),cv2.FILLED)
        cv2.putText(imgOut, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOut, (x - offset, y - offset),(x + w + offset, y + h + offset), (255, 0, 255), 4)

        cv2.imshow("imageCrop",imgCrop)
        cv2.imshow("imgWhite",imgWhite)
    cv2.imshow("image", imgOut)
    cv2.waitKey(1)

