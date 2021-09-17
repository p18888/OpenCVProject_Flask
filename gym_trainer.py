import cv2 as cv
import mediapipe as mp
import time
import PoseDetectionModule as pdm
import numpy as np
import math
import app1

def pushup_count():
    pTime=0
    cTime=0
    cap = cv.VideoCapture('static/push_ups3.mp4')
    img= cv.imread('static/push_up.jpg')
    detector =pdm.PoseDetection()
    count=0
    dir=0
    while True:
        _, img = cap.read()
        img=detector.findpose(img,False)
        lmlist = detector.findPosition(img,draw=False)
        if len(lmlist)!=0:
            angle=detector.fingAngles(img,12,14,16)
            per=np.interp(angle,(74,179),(0,100))
        if per == 0:
            if dir==0:
                count+=0.5
                dir=1
        if per == 100:
            if dir==1:
                count+=0.5
                dir=0

        img = cv.resize(img,(800,500))
        cv.putText(img,f'Puch up Count : {count}',(10,70),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
        img = cv.cvtColor(img,cv.COLOR_RGB2BGR)
        cv.imshow('image',img)
        k=cv.waitKey(1)
        if k==ord('q'):
            break
        else:
            pass
    cap.release()
    cv.destroyAllWindows()
    return app1.home()