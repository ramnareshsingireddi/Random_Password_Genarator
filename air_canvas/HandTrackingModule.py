import mediapipe as mp
import cv2 as cv
import time


class handDetector():
    def __init__(self,mode=False,maxHands=2,model_complexity=1,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands= maxHands
        self.model_complexity = model_complexity
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands = mp.solutions.hands
        self.hands= self.mpHands.Hands(self.mode,self.maxHands,self.model_complexity,self.detectionCon,self.trackCon)
        self.mpDraw =mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]


    def findHands(self,img,draw=True):
        imgRGB =cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                
                if draw:        #draw==true
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)  #It takes BGR image so it will take img
    
        return img
    
    
    def findPosition(self,img,handNo=0,draw=True):
        
        self.lmList =[]
        if self.results.multi_hand_landmarks:
            myHand =self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                #print(id,lm) it will print the id for hand landmarks and give corresponding landmark xyz values as well
                
                h,w,c=img.shape #hight widht chaneel of img
                cx,cy = int(lm.x*w),int(lm.y*h) #it will give center position of the landmark
                
                #print(id,cx,cy) it wills shows the senter postion of the id
                
                self.lmList.append([id,cx,cy])
                
                if draw:
                    cv.circle(img,(cx,cy),6,(0,255,0),cv.FILLED)
        return self.lmList
                
    def finguresUp(self):
        fingures=[]
        
        #tumb
        if self.lmList[self.tipIds[0]][1]<self.lmList [self.tipIds[0]-1][1]:
            fingures.append(1)
        else:
            fingures.append(0)
        
        #remainig 4 fingures
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2]<self.lmList[self.tipIds[id]-2][2]:
                
                fingures.append(1)
            else:
                
                fingures.append(0)
        return fingures 
            

        
def main():
    cTime=0 #current time
    pTime=0 #previos Time
    cap= cv.VideoCapture(0)
    detector = handDetector()

    while True:
        success,img = cap.read()
        img=detector.findHands(img)
        lmList = detector.findPosition(img)
        
        print(lmList)#it will prind hand id ad position (cx,xy)
        
        
        cTime=time.time()
        fps =1/(cTime - pTime) #leave it for now
        pTime =cTime
        
        cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_COMPLEX,3,(255,0,0),2)
        
        
        cv.imshow("image",img)
        cv.waitKey(20)
        
    

if __name__== "__main__":
    main()