import math
import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)
deteksi = HandDetector(detectionCon=0.8)

#membuat objek tombol

class tombol:

    def __init__(self,pos,lebar,tinggi,nilai):
        self.pos = pos
        self.lebar = lebar
        self.tinggi = tinggi
        self.nilai = nilai

    def gambarTombol(self,img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.lebar, self.pos[1] + self.tinggi),
                      (225, 191, 0), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.lebar, self.pos[1] + self.tinggi),
                      (50, 50, 50), 3)
        cv2.putText(img, self.nilai, (self.pos[0] + 30, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)
    def checkClick(self, cursor):
        if self.pos[0] < cursor[0] < self.pos[0] + self.lebar and \
                self.pos[1] < cursor[1] < self.pos[1] + self.tinggi:
         
            cv2.rectangle(img, (self.pos[0] + 1, self.pos[1] + 1),
                          (self.pos[0] + self.lebar - 3, self.pos[1] + self.tinggi - 3),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.nilai, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)
            return True
        else:
            return False
nilaiTombol_2D = [['7', '8', '9', '*','CE'],
                  ['4', '5', '6', '-','**'],
                  ['1', '2', '3', '+','sqrt'],
                  ['0', '/', '.', '=','C']]
nilaiTombol_1D = []

for X in range(5):
    for Y in range(4):
        xpos = X*100+700
        ypos = Y*100 + 150
        nilaiTombol_1D.append(tombol((xpos, ypos), 150, 150, nilaiTombol_2D[Y][X]))

nilaiAngkaYangmasuk = ''


l = len(nilaiAngkaYangmasuk)        
while True:
    sukses, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = deteksi.findHands(img, flipType=False)
    cv2.rectangle(img, (700, 40), (800 + 450, 70 + 100),
                  (75, 83, 32), cv2.FILLED)
 
    cv2.rectangle(img, (700, 40), (800 + 450, 70 + 100),
                  (50, 50, 50), 3)
    for tombol in nilaiTombol_1D:
        tombol.gambarTombol(img)
    if hands:
        # Find distance between fingers
        lmList = hands[0]['lmList']
        length, info, img = deteksi.findDistance(lmList[8], lmList[12], img)
        
        cursor = lmList[8]
        print(cursor)   
        # If clicked check which button and perform action
    try:
        if length < 50 :
            for i,tombol in enumerate(nilaiTombol_1D):

                if tombol.checkClick(cursor):

                    nilaiPerhitungan = nilaiTombol_2D[int(i % 4)][int(i / 4)]
            
                    if nilaiPerhitungan == '=':
                        nilaiAngkaYangmasuk = str(eval(nilaiAngkaYangmasuk))
                    elif nilaiPerhitungan == 'CE':
                        #nilaiAngkaYangmasuk = nilaiAngkaYangmasuk.rstrip(nilaiAngkaYangmasuk[-1])
                        

                        nilaiAngkaYangmasuk = nilaiAngkaYangmasuk[:l-1]
                    elif nilaiPerhitungan == 'C':
                        #nilaiAngkaYangmasuk = nilaiAngkaYangmasuk.rstrip(nilaiAngkaYangmasuk[-1])
                        

                        nilaiAngkaYangmasuk=''
                    elif nilaiPerhitungan == 'sqrt':
                        #nilaiAngkaYangmasuk_akar += nilaiPerhitungan
                      
                        nilaiAngkaYangmasuk_1= math.sqrt(eval(nilaiAngkaYangmasuk))
                        nilaiAngkaYangmasuk_1=float("{:.2f}".format(nilaiAngkaYangmasuk_1))
                        nilaiAngkaYangmasuk = str(nilaiAngkaYangmasuk_1)
                        
                    else:
                        nilaiAngkaYangmasuk += nilaiPerhitungan
                    time.sleep(0.3)
    except:
            print('error')
                

                  
                   
    cv2.putText(img, nilaiAngkaYangmasuk, (710, 130), cv2.FONT_HERSHEY_PLAIN,
                3, (255,255,255), 3)
    
    cv2.waitKey(1)
    cv2.imshow("Img",img)
    