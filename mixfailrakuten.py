from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import xml.etree.ElementTree as et
import time
from lxml import html
from bs4 import BeautifulSoup
import requests
import os
import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
import json

# 楽天商品検索API (BooksGenre/Search/)のURL
RAKUTEN_BOOKS_API_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
RAKUTEN_APP_ID = "1005881074603863189"

import MySQLdb

# 接続する
conn = MySQLdb.connect(
user='root',
passwd='',
host='localhost',
# db='mysql'
db='book')

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
            
            # 楽天商品検索API (BooksGenre/Search/)のURL
            url = RAKUTEN_BOOKS_API_URL
            # URLのパラメータ
            param = {
                # 前手順で取得したアプリIDを設定する
                "applicationId" : RAKUTEN_APP_ID,
                "isbn" : myData,
                "format" : "json"
            }
            
            # APIを実行して結果を取得する
            result = requests.get(url, param)
            # json_result = result.json()
            json_result = json.loads(result.text)
            dict_result = {}
            print("リザルト")
            # print(json_result)
            # タイトル
            title = json_result['Items'][0]['Item']['title']
            # 作者
            author = json_result['Items'][0]['Item']['author']
            # 巻数
            availability = json_result['Items'][0]['Item']['availability']
            # isbn
            isbn = json_result['Items'][0]['Item']['isbn']
            # 金額
            price = json_result['Items'][0]['Item']['itemPrice']
            # 出版者
            publisherName = json_result['Items'][0]['Item']['publisherName']
            # 出版者
            # publisherName = json_result['Items'][0]['Item']['publisherName']
            print(title)
            print(author)
            print(availability)
            print(isbn)
            print(price)

            # カーソルを取得する
            cur = conn.cursor()
            sql = "INSERT INTO bookinfo (ISBN, Title, Creator , availability , money , status) VALUES ('"+ str(isbn) +"' , '" + str(title) +"' , '" + str(author) + "'," + str(availability) + " , '" + str(price) + "', 0 )"
            print(sql)
            cur.execute(sql)
            cur.close()
            conn.commit()
            time.sleep(2)
            
        #QRコードの周りに長方形を描画しデータを表示する
        pts =np.array([barcode.polygon],np.int32)
        #polylines()関数で複数の折れ線を描画
        cv.polylines(frame,[pts],True,(255,0,0),5)
        pts2 =barcode.rect
        #putText()関数で文字列を描画
        cv.putText(frame,myData,(pts2[0],pts2[1]),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)

    #imshow()関数で出力ウィンドウを表示
    cv.imshow('test',frame)
    k = cv.waitKey(1)
    val = cv.getWindowProperty('test' , cv.WND_PROP_ASPECT_RATIO)
    if(val < 0):
        break
    
conn.close()
cap.release()
cv.destroyAllWindows()

