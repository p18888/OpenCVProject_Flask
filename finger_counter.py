import cv2 as cv
import mediapipe as mp
import time
import HandTrackerModule as htm
import numpy as np
import math
import app1




def get_fingers(fingers,lmlist,tip_ids):
    ##  For left thumb
    if lmlist[tip_ids[0]][1] > lmlist[tip_ids[0]-1][1]:
        fingers.append(1)
    else:
        fingers.append(0)
        ## For rest fingers
    for i in range(1,5):
        if lmlist[tip_ids[i]][2] < lmlist[tip_ids[i]-2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def count_finger():
    pTime=0
    cTime=0
    # link ='http://192.168.0.101:8080/video'
    cap = cv.VideoCapture(0)
    detector =htm.handTracker()


    fing_lis_path = ['static/0.jpg','static/1.png','static/2.png','static/3.jpg','static/4.jpg',
    'static/5.jpg','static/6.jpg','static/7.jpg','static/8.jpg','static/9.jpg','static/10.jpg']
    ovelaylist=[]
    for path in fing_lis_path:
        img=cv.imread(path)
        img=cv.resize(img,(255,197))
        ovelaylist.append(img)
    tip_ids=[4,8,12,16,20]

    while True:
        _,frame = cap.read()
        frame=detector.findhands(frame)
        frame=cv.resize(frame,(750,550))
        lmlist=detector.findPosition(frame)
        if len(lmlist)!=0:
            fingers=[]
            ## for thumb
            if lmlist[tip_ids[0]][1] < lmlist[tip_ids[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
                ## For rest fingers
            for i in range(1,5):
                if lmlist[tip_ids[i]][2] < lmlist[tip_ids[i]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            if len(lmlist)>21:
                fingers=get_fingers(fingers,lmlist[21:],tip_ids)
            else:
                pass
            
            fing_count=fingers.count(1)
            h,w,c=ovelaylist[fing_count].shape
            frame[:h,:w,:c] = ovelaylist[fing_count]

            cv.putText(frame,str(fingers.count(1)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv.putText(frame,f'FPS: {str(int(fps))}',(560,50),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),3)
        frame = cv.cvtColor(frame,cv.COLOR_RGB2BGR)
        cv.imshow('image',frame)
        k=cv.waitKey(1)
        if k==ord('q'):
            break
        else:
            pass
    cap.release()
    cv.destroyAllWindows()
    return app1.home()
