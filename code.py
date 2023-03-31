import cv2
import numpy as np
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,170)

clr=cv2.imread("Resources/palette.png")
cv2.imshow("choose",clr)

b,g,r=0,0,0
myPoints=[]

def choice(event,x,y,flags,param):
    global b,g,r
    if event==cv2.EVENT_LBUTTONDBLCLK:
        global xpos,ypos,clicked
        clicked=True
        xpos=x
        ypos=y
        b,g,r=clr[y,x]
        b=int(b)
        g=int(g)
        r=int(r)
        #print (b," ",g," ",r)

cv2.setMouseCallback("choose", choice)

def find_blackpen(img):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #cv2.imshow("hsv",imgHSV)
    newPts=[]
    lower = np.array([52, 0, 0])
    upper = np.array([179, 254, 110])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    x,y=getContours(mask)
   # b,g,r=choice()
    cv2.circle(imgRes,(x,y),4,(b,g,r),5,cv2.FILLED)
    if x!=0 and y!=0:
        newPts.append([x,y,b,g,r])
    return newPts

def drawOnScreen(myPoints,b,g,r):
    for pts in myPoints:
        cv2.circle(imgRes, (pts[0], pts[1]), 4, (pts[2], pts[3], pts[4]), 5, cv2.FILLED)

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgRes, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

while True:
    succ,img=cap.read()
    imgRes=img.copy()
    newPts=find_blackpen(img)
    if len(newPts)!= 0:
        for newP in newPts:
            myPoints.append(newP)
    if len(myPoints)!= 0:
        drawOnScreen(myPoints,b,g,r)
    print(b," ",g," ",r)
    imgRes=cv2.flip(imgRes,1)
    cv2.imshow("out",imgRes)


    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
