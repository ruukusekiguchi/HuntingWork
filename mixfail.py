from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from lxml import html
from bs4 import BeautifulSoup
import requests
import os
import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode

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
            print(myData)
            option = Options()# オプションを用意
            option.add_argument('--headless') 
            driver = webdriver.Chrome(options=option) 
            # driver = webdriver.Chrome(executable_path='./chromedriver.exe')
            driver.maximize_window()
            driver.get('https://www.bookliner.co.jp/bl/view/display-customer-menu.action')
            elem = driver.find_element_by_id("search")
            elem.send_keys(myData)
            clickelem = driver.find_element_by_xpath('//*[@id="fuzzySearchForm"]/input[3]')
            clickelem.click()

            current_url = driver.current_url
            html = requests.get(current_url)
            bs = BeautifulSoup(html.text, "lxml")
            name = driver.find_element_by_xpath('//*[@id="listItemForm"]/div[6]/div/div[2]/div[2]/table[1]/tbody/tr/td[2]/h4/a')
            name.click()
            # elem = driver.find_element_by_id("search")
            title = driver.find_element_by_xpath('//*[@id="displayDetailForm"]/div[2]/div[1]/div[2]/h4').text
            makename = driver.find_element_by_xpath('//*[@id="displayDetailForm"]/div[2]/div[1]/div[2]/table[1]/tbody/tr[2]/td').text
            makeshuppan = driver.find_element_by_xpath('//*[@id="displayDetailForm"]/div[2]/div[1]/div[2]/table[2]/tbody/tr[1]/td').text
            money = driver.find_element_by_xpath('//*[@id="displayDetailForm"]/div[2]/div[1]/div[2]/table[2]/tbody/tr[4]/td').text

            # カーソルを取得する
            cur = conn.cursor()
            sql = "INSERT INTO bookinfo (ISBN, Title, Creator , money) VALUES ("+ myData +",'" + title +"' , '"+ makename.strip() + "' , '" + money.strip() + "' )"
            print(sql)
            cur.execute(sql)
            cur.close()
            conn.commit()
            
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

