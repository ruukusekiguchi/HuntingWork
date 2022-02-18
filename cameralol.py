import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode

#Webカメラの読み込み
cap = cv.VideoCapture(1)
#出力ウィンドウの設定
cap.set(3,640)
cap.set(3,480)

while True:
    #カメラから1コマのデータを取得する
    ret,frame = cap.read()
    #バーコードからデータを読み取る
    for barcode in decode(frame):
        # print(barcode.data)
        #QRコードデータはバイトオブジェクトなので、カメラ上に描くために、文字列に変換する
        myData = barcode.data.decode('utf-8')
        if(myData.startswith('9784')):
            print(myData)

            
        #QRコードの周りに長方形を描画しデータを表示する
        pts =np.array([barcode.polygon],np.int32)
        #polylines()関数で複数の折れ線を描画
        cv.polylines(frame,[pts],True,(255,0,0),5)
        pts2 =barcode.rect
        #putText()関数で文字列を描画
        cv.putText(frame,myData,(pts2[0],pts2[1]),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)

    # if(myData.find('9784')):
    #     print(myData)

    #imshow()関数で出力ウィンドウを表示
    cv.imshow('test',frame)
    k = cv.waitKey(1)
    val = cv.getWindowProperty('test' , cv.WND_PROP_ASPECT_RATIO)
    if(val < 0):
        break
    

cap.release()
cv.destroyAllWindows()

    # if cv.waitKey(1) & 0xFF == ord('q'):
    #     break