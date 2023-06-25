import threading
import time
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math



detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

labels = []
with open('Model\labels.txt', 'r') as file:
    for line in file:
        index, label = line.strip().split(' ', 1)
        labels.append(label)

timer = 3
isTimerRunning = False
predictionLetter = None


def detectSign(imgOutput):
    global isTimerRunning, predictionLetter
    if not isTimerRunning:
        return False # dont detect words without timer
    try:
        hands, img = detector.findHands(imgOutput)
        if hands:
            
            hand = hands[0]
            x, y, w, h = hand['bbox']
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
            imgCropShape = imgCrop.shape
            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)


            if timer > 1:
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                            (x - offset + 210, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
                cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
                cv2.putText(imgOutput, "Picker Timer = " + str(timer), (x, y - 76), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                predictionLetter = labels[index]
            else:
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                            (x - offset + 210, y - offset - 50 + 50), (43, 255, 0), cv2.FILLED)
                cv2.putText(imgOutput, predictionLetter, (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
                cv2.putText(imgOutput, "Picker Timer = " + str(timer), (x, y - 76), cv2.FONT_HERSHEY_COMPLEX, 1, (43, 255, 0), 2)
            return predictionLetter
        else:
            predictionLetter = None
            return False
    except Exception as e:
        print("ERROR: update_image()",e)
        predictionLetter = None
        return False

        

    
def startTimer(sec = 3):
    global timer, predictionLetter
    if not isTimerRunning:
        timer = sec
        thread = threading.Thread(target=updateTimer)
        thread.start()
        thread.join()
        return predictionLetter
    return False

def updateTimer():
    global isTimerRunning, timer
    isTimerRunning = True
    while(timer > 0):
        time.sleep(1)
        timer -= 1
    isTimerRunning = False
    



        