import cv2 as cv
import os
import numpy as np
import HandTrackingModule as htm

folderPath ="header"

myList=os.listdir(folderPath)
#print(myList)
overlayList=[]

for imPath in myList:
    image = cv.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
    
header = overlayList[0]
drawColor=(255,0,255)
brushThickness=15
eraserThickness=50


cap =cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=htm.handDetector(detectionCon=0.85)


imgCanvas = np.zeros((720,1280,3),np.uint8) #unshined interger of 8 bits (0-255)=uint8

while True:
    success,img = cap.read()
    
    
    #1.setting the header img
    img=cv.flip(img,1) #use full drow properly
    img[0:125,0:1280]= header

    
    #2.find hand landmarks
    
    img= detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    
    if len(lmList)!=0:
        #print(lmList)
        #tip of our index fingure
        x1,y1=lmList[8][1:] #to elminate id     
        x2,y2=lmList[12][1:]#tip of midle fingure
        
    
         #3.check which finger are up
    
        fingers=detector.finguresUp()
        #print(fingers)
    
         #4.If selection mode when two fingers are up we have to select
        
        if fingers[1] and fingers[2]:
            
            # print("selection"
            
            xp,yp=0,0
            
            #checking for click
            if y1<125: #it means we are in the headre
                if 250< x1 <450:
                    header=overlayList[0]
                    drawColor=(255,0,255)
                elif 450< x1 <650:
                    header=overlayList[1]
                    drawColor=(255,0,0)
                    
                elif 800< x1 <950:
                    header=overlayList[2]
                    drawColor=(0,255,0)
                elif 1050< x1 <1200:
                    header=overlayList[3]
                    drawColor=(0,0,0)
                    
            cv.rectangle(img,(x1,y1-30),(x2,y2+30),drawColor,cv.FILLED)
                    
            
             
        #5. If Drawing mode when Index finger is up
        if fingers[1] and fingers[2]==False:
            #print("draw")
            cv.circle(img,(x1,y1),15,drawColor,cv.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1
                
            if  drawColor==(0,0,0):
                cv.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                
                cv.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
                
            else:
                    
                cv.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                
                cv.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
                
            xp,yp=x1,y1
        
    
    

    
    #img=cv.addWeighted(img,0.5,imgCanvas,0.5,0)   it shows the draw in some tranpernce so we wite bello code
    
    imgGray = cv.cvtColor(imgCanvas,cv.COLOR_BGR2GRAY)
    _,imgInv = cv.threshold(imgGray,50,255,cv.THRESH_BINARY_INV) #convert to binarry help to bello code
    
    imgInv = cv.cvtColor(imgInv,cv.COLOR_GRAY2BGR)
    img=cv.bitwise_and(img,imgInv)
    img=cv.bitwise_or(img,imgCanvas)
    
    
    
    cv.imshow("IMAGE",img)
    cv.waitKey(10)