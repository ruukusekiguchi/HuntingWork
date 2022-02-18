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

# 楽天商品検索API (BooksGenre/Search/)のURL
url = RAKUTEN_BOOKS_API_URL
# URLのパラメータ
param = {
    # 前手順で取得したアプリIDを設定する
    "applicationId" : RAKUTEN_APP_ID,
    "isbn" : 9784758023115,
    "format" : "json"
}
            
# APIを実行して結果を取得する
result = requests.get(url, param)
# json_result = result.json()
json_result = json.loads(result.text)
dict_result = {}
print("リザルト")
print(json_result)