from cvzone.HandTrackingModule import HandDetector
import cv2
import socket
import pyautogui
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
success, img = cap.read()
h, w, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)
tipIds = [4, 8, 12, 16, 20]

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    #hands = detector.findHands(img, draw=False)  # without draw
    data = []

    if hands:
        if len(hands)==2:
            hand1 = hands[0]
            hand2 = hands[1]

            lmList1 = hand1["lmList"]
            lmList2 = hand2["lmList"]

            rList=[]
            lList=[]
            print(lmList1[4][0]," : ",lmList1[20][0])
            if(lmList1[4][0]>lmList1[20][0]):
                rList = lmList1
                lList = lmList2
            else:
                rList = lmList2
                lList = lmList1



            # Right Hand
            rfingers = []

            # Thumb
            if rList[tipIds[0]][0] > rList[tipIds[1]][0]:
                rfingers.append(1)
            else:
                rfingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if rList[tipIds[id]][1] < rList[tipIds[id] - 2][1]:
                    rfingers.append(1)
                else:
                    rfingers.append(0)

            # print(fingers)
            rdata = rfingers.count(1)





            # Left Hand
            lfingers = []

            # Thumb
            if lList[tipIds[0]][0] < lList[tipIds[1]][0]:
                lfingers.append(1)
            else:
                lfingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lList[tipIds[id]][1] < lList[tipIds[id] - 2][1]:
                    lfingers.append(1)
                else:
                    lfingers.append(0)

            # print(fingers)
            ldata = lfingers.count(1)
            print("Left hand : ", ldata,"    Right Hand : ",rdata)




            if ldata == 1:
                #print("hello")
                if rdata == 1:
                    #print("HI")
                    pyautogui.keyDown('up')
                    time.sleep(0.5)
                    pyautogui.keyUp('up')

                elif rdata == 2:
                    pyautogui.keyDown('down')
                    time.sleep(0.5)
                    pyautogui.keyUp('down')


                elif rdata == 3:
                    pyautogui.keyDown('right')
                    time.sleep(0.5)
                    pyautogui.keyUp('right')

                elif rdata == 4:
                    pyautogui.keyDown('left')
                    time.sleep(0.5)
                    pyautogui.keyUp('left')



            elif ldata == 5:
                if rdata == 1:
                    pyautogui.keyDown('space')
                    pyautogui.keyDown('up')
                    time.sleep(0.5)
                    pyautogui.keyUp('up')
                    pyautogui.keyUp('space')

                elif rdata == 2:
                    pyautogui.keyDown('space')
                    pyautogui.keyDown('down')
                    time.sleep(0.5)
                    pyautogui.keyUp('down')
                    pyautogui.keyUp('space')

                elif rdata == 3:
                    pyautogui.keyDown('space')
                    pyautogui.keyDown('right')
                    time.sleep(0.5)
                    pyautogui.keyUp('right')
                    pyautogui.keyUp('space')

                elif rdata == 4:
                    pyautogui.keyDown('space')
                    pyautogui.keyDown('left')
                    time.sleep(0.5)
                    pyautogui.keyUp('left')
                    pyautogui.keyUp('space')




        #sock.sendto(str.encode(str(data)), serverAddressPort)

    # Display
    img = cv2.resize(img,(0,0),None,0.5,0.5)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()