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

# ヘッドレスモード（画面を出してスクリーンショットすると、全体が撮れないため）
driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.maximize_window()

driver.get('https://www.bookliner.co.jp/bl/view/display-customer-menu.action')
elem = driver.find_element_by_id("search")
elem.send_keys("9784088918723")
clickelem = driver.find_element_by_xpath('//*[@id="fuzzySearchForm"]/input[3]')
clickelem.click()

print(1)
time.sleep(5)
current_url = driver.current_url
html = requests.get(current_url)
bs = BeautifulSoup(html.text, "lxml")
print(2)
# element = driver.find_element_by_xpath(bs)
# elem = driver.find_element_by_id("check_0")
# elm = driver.find_element_by_xpath('//*[@id="listItemForm"]/div[6]/div/div[2]/div[1]/a/img')
# actions = ActionChains(driver)
# actions.move_to_element(elem)
# actions.perform()
print(3)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# element = driver.find_by_xpath('//*[@id="listItemForm"]/div[6]/div/div[2]/div[1]/a/img').screenshot_as_png
src = driver.find_element_by_xpath('//*[@id="listItemForm"]/div[6]/div/div[2]/div[1]/a/img')
# actions = ActionChains(driver)
# print("deiver=")
# print(driver)
# actions.move_to_element(src)
# actions.perform()

# src = driver.find_element_by_xpath('//*[@id="listItemForm"]/div[6]/div/div[2]/div[1]/a/img').screenshot_as_png
# ActionChains(driver).move_to_element(src).perform()

print(4)
# イメージ保存
with open('./img.png', 'wb') as f:
    f.write(src)
print(5)
driver.quit()
