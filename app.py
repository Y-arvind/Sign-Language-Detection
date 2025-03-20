import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Error: Could not open webcam.")

    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

    offset = 20
    imgSize = 300
    labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z"]

    while True:
        success, img = cap.read()
        if not success:
            print("Warning: Failed to read frame from webcam.")
            continue

        imgOut = img.copy()
        hands, img = detector.findHands(img)

        if hands:
            try:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

                # Ensure valid cropping bounds
                y1, y2 = max(0, y - offset), min(img.shape[0], y + h + offset)
                x1, x2 = max(0, x - offset), min(img.shape[1], x + w + offset)
                imgCrop = img[y1:y2, x1:x2]

                if imgCrop.size == 0:
                    print("Warning: Cropped image is empty, skipping frame.")
                    continue

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wGap + wCal] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hGap + hCal, :] = imgResize

                prediction, index = classifier.getPrediction(imgWhite, draw=False)

                cv2.rectangle(imgOut, (x - offset, y - offset - 50), (x - offset + 90, y - offset + 50), (255, 0, 255),
                              cv2.FILLED)
                cv2.putText(imgOut, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
                cv2.rectangle(imgOut, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255), 4)

                cv2.imshow("imageCrop", imgCrop)
                cv2.imshow("imgWhite", imgWhite)
            except Exception as e:
                print(f"Error processing hand detection: {e}")

        cv2.imshow("image", imgOut)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    print(f"Critical error: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()