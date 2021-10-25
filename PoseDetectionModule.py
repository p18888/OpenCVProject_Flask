import cv2 as cv
import mediapipe as mp
import time 
import numpy as np
import math

class PoseDetection():
    def __init__(self,mode=False,modelc=1,smooth=True,enbl_seg=False,smooth_seg=True,
     detectionCon=0.5,trackCon=0.5):

        self.mode=mode
        self.modelc=modelc
        self.smooth=smooth
        self.enbl_seg=enbl_seg
        self.smooth_seg=smooth_seg
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.modelc,self.smooth,self.enbl_seg,
        self.smooth_seg,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findpose(self,frame,draw=True):
        frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        frame=cv.flip(frame,1)
        frame=cv.resize(frame,(500,500))
        self.result = self.pose.process(frame)
        if draw:
            if self.result.pose_landmarks:
                self.mpDraw.draw_landmarks(frame,self.result.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return frame

    def findPosition(self,frame,handNo=0,draw=True):
        self.lmlist=[]
        if self.result.pose_landmarks:
            for id,lm in enumerate(self.result.pose_landmarks.landmark):
                # print("id",id,"lm",lm)
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv.circle(frame,(cx,cy),6,(255,0,0),cv.FILLED)
        
        return self.lmlist

    def fingAngles(self,frame,p1,p2,p3,draw=True):
        x1,y1=self.lmlist[p1][1:]
        x2,y2=self.lmlist[p2][1:]
        x3,y3=self.lmlist[p3][1:]
        if draw:
            cv.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv.line(frame,(x2,y2),(x3,y3),(0,255,0),2)
            cv.circle(frame,(x1,y1),10,(255,0,0),cv.FILLED)
            cv.circle(frame,(x1,y1),15,(0,0,255),2)
            cv.circle(frame,(x2,y2),10,(255,0,0),cv.FILLED)
            cv.circle(frame,(x2,y2),15,(0,0,255),2)
            cv.circle(frame,(x3,y3),10,(255,0,0),cv.FILLED)
            cv.circle(frame,(x3,y3),15,(0,0,255),2)
            angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
            cv.putText(frame,str(int(angle)),(x2+25,y2),cv.FONT_HERSHEY_PLAIN,3,(0,0,255),2)
            return angle


def main():
    pTime= 0
    cTime=0
    cap=cv.VideoCapture('vidios/dance.mp4')
    detector=PoseDetection()
    while True:
        isTrue,frame=cap.read()
        frame=cv.resize(frame,(700,700))
        frame=detector.findpose(frame)
        lmlist=detector.findPosition(frame)
        if len(lmlist)!=0:
            print(lmlist[4])        
            cv.circle(frame,(lmlist[14][1],lmlist[14][2]),15,(0,0,255),cv.FILLED)



        cTime=time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv.imshow('Vidio',frame)
        k=cv.waitKey(1)
        if k==ord('q'):
            break


if __name__ == '__main__':
    main()