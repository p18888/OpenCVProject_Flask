import cvzone
import os
import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import app

def change_background():
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    segmentor = SelfiSegmentation()
    fps_reader=cvzone.FPS()

    bckimg_lis=os.listdir(r'E:\OpenCVProject_Flask\static\background')

    lis=[(0,0,0)]
    for i in bckimg_lis:
        img=cv2.imread(r'E:\OpenCVProject_Flask\static\background\{}'.format(i))
        img=cv2.resize(img,(640,480))
        lis.append(img)
    id=0

    while True:
        _,frame = cap.read()
        frame=cv2.flip(frame,1)
        # print(frame.shape)
        imgOut = segmentor.removeBG(frame,lis[id],threshold=0.1)
        stack_img=cvzone.stackImages([frame,imgOut],2,1)
        _,stack_img=fps_reader.update(stack_img)
        cv2.imshow("Image",stack_img)

        key=cv2.waitKey(1)

        if key == ord("d"):   ## d == for change background
            if id <len(lis)-1:
                id += 1
            else:
                id=0
        elif key == ord("a"): ## a == for previous background
            if id !=0:
                id -=1
            else:
                id=0
        elif key == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    return app.home()