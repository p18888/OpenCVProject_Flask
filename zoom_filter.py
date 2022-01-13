
import cv2 as cv
import cvzone
import mediapipe as mp
import math
import numpy as np
import app

def image_zoom():
    cap=cv.VideoCapture(0)
    fps_reader=cvzone.FPS()
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                        max_num_hands=2,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils

    id=0
    while True:
        _,frame=cap.read()
        frame=cv.resize(frame,(750,550))
        frame=cv.flip(frame,1)

        height, width,clr= frame.shape

        results = hands.process(frame)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                try:
                    x1,y1=int(handLms.landmark[4].x*width),int(handLms.landmark[4].y*height)
                    x2,y2=int(handLms.landmark[8].x*width),int(handLms.landmark[8].y*height)
                except:
                    break

                cx,cy = (x1+x2)//2,(y1+y2)//2
                cv.circle(frame,(x1,y1),6,(255,0,0),cv.FILLED)
                cv.circle(frame,(x2,y2),6,(255,0,0),cv.FILLED)

                length  = math.sqrt((x2-x1)**2+(y2-y1)**2)

                if int(length) in list(range(70,160)):
                    cv.line(frame,(x1,y1),(x2,y2),(255,0,255),3,cv.FILLED)
                    vol=np.interp(length,[70,160],[10,1])
                    id =int(vol)
                else:
                    id=0
        if id !=0:
            cropped=frame[height//id:height-(height//id),width//id:width-(width//id)]
        else:
            cropped=frame
        try:
            cropped=cv.resize(cropped,(750,550))
        except:
            cropped=frame

        _,stack_img=fps_reader.update(frame)
        cv.imshow("Image",frame)
        cv.imshow("Cropped",cropped)
        k=cv.waitKey(1)
        if k==ord("q"):
            break
    cap.release()
    cv.destroyAllWindows()
    return app.home()

