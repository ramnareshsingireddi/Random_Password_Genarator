import mediapipe as mp
import cv2 as cv
import time


cap= cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands= mpHands.Hands()
mpDraw =mp.solutions.drawing_utils
cTime=0 #current time
pTime=0 #previos Time

while True:
    success,img = cap.read()
    imgRGB =cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            
            for id,lm in enumerate(handLms.landmark):
                #print(id,lm) it will print the id for hand landmarks and give corresponding landmark xyz values as well
                
                h,w,c=img.shape #hight widht chaneel of img
                cx,cy = int(lm.x*w),int(lm.y*h) #it will give center position of the landmark
                
                #print(id,cx,cy) it wills shows the senter postion of the id
                
                if id ==8:
                    cv.circle(img,(cx,cy),15,(0,255,0),cv.FILLED)
                
                
                
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)  #It takes BGR image so it will take img
    
    cTime=time.time()
    fps =1/(cTime - pTime) #leave it for now
    ptime =cTime
    
    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_COMPLEX,3,(255,0,0),2)
    
    
            
        
    
    cv.imshow("image",img)
    cv.waitKey(20)