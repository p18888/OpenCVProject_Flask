import cv2 as cv
import numpy as np
import mediapipe as mp
import time 




class handTracker():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands=mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tip_ids = [4,8,12,16,20]

    
    def findhands(self,frame,draw=True):
        frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        frame=cv.flip(frame,1)
        # frame=cv.resize(frame,(500,500))
        self.result = self.hands.process(frame)
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame,handLms,self.mpHands.HAND_CONNECTIONS)
                # for id,lm in enumerate(handLms.landmark):
                #     print("id",id,"lm",lm)
                #     h,w,c=frame.shape
                #     cx,cy=int(lm.x*w),int(lm.y*h)

                #     if id==4:
                #         cv.circle(frame,(cx,cy),15,(255,0,0),cv.FILLED)
        return frame
    def findPosition(self,frame,handNo=0,draw=True):
        self.lmlist=[]
        if self.result.multi_hand_landmarks:
            # handLms=self.result.multi_hand_landmarks[handNo]
            for handLms in self.result.multi_hand_landmarks:
                for id,lm in enumerate(handLms.landmark):
                    # print("id",id,"lm",lm)
                    h,w,c=frame.shape
                    cx,cy=int(lm.x*w),int(lm.y*h)
                    self.lmlist.append([id,cx,cy])
                    if draw:
                        cv.circle(frame,(cx,cy),8,(255,0,0),cv.FILLED)
        
        return self.lmlist

    def get_fingersUp(self):
        fingers=[]
        ## for thumb
        if self.lmlist[self.tip_ids[0]][1] < self.lmlist[self.tip_ids[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
            ## For rest fingers
        for i in range(1,5):
            if self.lmlist[self.tip_ids[i]][2] < self.lmlist[self.tip_ids[i]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers



def main():
    pTime= 0
    cTime=0
    link ='http://192.168.0.101:8080/video'
    cap = cv.VideoCapture(0)
    detector = handTracker()
    while cap.open(link):
        success,frame = cap.read()
        frame=detector.finghands(frame)
        lmlist=detector.findPosition(frame)
        # print(lmlist)
        if len(lmlist)!=0:
            print(lmlist[4])
        cTime = time.time()
        fps = 1 / (cTime-pTime)
        pTime = cTime

        cv.putText(frame,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        frame = cv.cvtColor(frame,cv.COLOR_RGB2BGR)
        cv.imshow('image',frame)
        k=cv.waitKey(25)
        if k==ord('q'):
            break


if __name__=='__main__':
    main()