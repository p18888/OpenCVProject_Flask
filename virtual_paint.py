import cv2 as cv
import mediapipe as mp
import time
import HandTrackerModule as htm
import numpy as np
import math
import os
import app1


folder_path='static/paint_headers'
myList=os.listdir(folder_path)
ovelayList=[]
for path in myList:
    img=cv.imread(f'{folder_path}/{path}')
    img=cv.resize(img,(640,124))
    # img=cv.flip(img,1)
    ovelayList.append(img)

def paint_virtual():
    pTime= 0
    cTime=0
    cap = cv.VideoCapture(0)
    detector = htm.handTracker()

    drawing_clr=(255,0,255)
    brush_thickness=15

    canvas_img=np.zeros((480,640,3),dtype=np.uint8)
    header=ovelayList[5]
    xp,yp=0,0
    while True:
        _,frame = cap.read()

        frame=detector.findhands(frame)
        lmlist=detector.findPosition(frame,draw=False)

        if len(lmlist)!=0:
            x1,y1=lmlist[8][1:]  ## fore finger
            x2,y2=lmlist[12][1:] ## Middle finger

            fingers=detector.get_fingersUp()

            if fingers[1]==1 and fingers[2]==1:
                xp,yp=0,0
                cv.rectangle(frame,(x1,y1),(x2,y2),drawing_clr,25,cv.FILLED)
                if y1 in range(0,100):
                    if x1 in range(100,180):
                        drawing_clr=(0,0,255)
                        cv.rectangle(frame,(x1,y1),(x2,y2),drawing_clr,25,cv.FILLED)
                        header = ovelayList[0]
                    if x1 in range(200,280):
                        drawing_clr=(0,255,0)
                        cv.rectangle(frame,(x1,y1),(x2,y2),drawing_clr,25,cv.FILLED)
                        header = ovelayList[1]
                    if x1 in range(300,380):
                        drawing_clr=(255,0,0)
                        cv.rectangle(frame,(x1,y1),(x2,y2),drawing_clr,25,cv.FILLED)
                        header = ovelayList[2]
                    if x1 in range(400,480):
                        drawing_clr=(255,255,255)
                        cv.rectangle(frame,(x1,y1),(x2,y2),drawing_clr,25,cv.FILLED)
                        header = ovelayList[3]
                    if x1 in range(500,580):
                        drawing_clr=(0,0,0)
                        cv.rectangle(frame,(x1,y1),(x2,y2),drawing_clr,25,cv.FILLED)
                        header = ovelayList[4]

            if fingers[1]==1 and fingers[2]==0:
                cv.circle(frame,(x1,y1),15,drawing_clr,cv.FILLED)
                if xp==0 and yp==0:
                    xp,yp=x1,y1

                if drawing_clr==(0,0,0):
                    brush_thickness=80
                else:
                    brush_thickness=15
                cv.line(frame,(x1,y1),(xp,yp),drawing_clr,brush_thickness)
                cv.line(canvas_img,(x1,y1),(xp,yp),drawing_clr,brush_thickness)
                xp,yp = x1,y1

        img_gray=cv.cvtColor(canvas_img,cv.COLOR_BGR2GRAY)
        _,img_inv = cv.threshold(img_gray,50,255,cv.THRESH_BINARY_INV)

        img_inv=cv.cvtColor(img_inv,cv.COLOR_GRAY2BGR)

        frame=cv.bitwise_and(frame,img_inv)
        frame =  cv.bitwise_or(frame,canvas_img)



        h,w,c = header.shape
        frame[:h,:w,:c] = header


        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv.putText(frame,f'FPS: {str(int(fps))}',(500,50),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),3)
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

