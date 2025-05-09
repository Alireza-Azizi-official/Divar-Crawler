import numpy as np
import pandas as pd
from selenium import webdriver
import sys
import time
from selenium.webdriver import ActionChains
import argparse
import getpass
from pyvirtualdisplay import Display
import requests
import os
import pandasql as psql
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
import datetime
import pandasql as psql

mahal_name = 'میرداماد'
url_path_friend = ""
path_org = os.getcwd()
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
profile = webdriver.Chrome()
profile.set_preference('browser.download.folderList', 2) # custom location 
profile.set_preference('browser.download.manager.showWhenStarting', False) 
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "image/png,image/jpeg")
driver = webdriver.Chrome(chrome_profile=profile) 
time.sleep(2)
driver.maximize_window()
driver.get("https://divar.ir/s/tehran/buy-apartment") 
driver.find_element_by_id("u_0_d_d2").click()
time.sleep(2)
driver.get("https://divar.ir/s/tehran/buy-apartment") 
#driver.find_element_by_id("u_0_d_d2").click()
time.sleep(2)
#driver.find_element_by_xpath("//p[contains(.,'Consent')]").click()
driver.find_element(By.XPATH,"//span[contains(.,'قیمت')]").click()
time.sleep(1)
driver.find_element(By.XPATH,"//p[contains(.,'مثلا ۱،۰۰۰،۰۰۰،۰۰۰')]").click()
time.sleep(1)
driver.find_element(By.XPATH,"//li[contains(.,'وارد کردن مقدار دلخواه')]").click()
time.sleep(1)
gheimat_max = driver.find_element("id","max-1740827229")
gheimat_max_g = '350000000000'
gheimat_max.send_keys(gheimat_max_g)
time.sleep(1)
driver.find_element(By.XPATH,"//input[@class='kt-nav-text-field__input']").send_keys(mahal_name)
time.sleep(1)
driver.find_element(By.XPATH,"//p[contains(.,'در فروش آپارتمان')]").click()
df_news = pd.DataFrame(columns=[ 'title' , 'price_t' , 'amlak' ]  )
for i in range(10):
    title_1_8 = driver.find_elements(By.XPATH,"//div//div//div//div//a//article//div[@class='kt-post-card__body']")
    for my_href in title_1_8:
        print(my_href.text)
        print('*****************************************************')
        string_file = my_href.text
        if string_file != '':
            string_file = string_file.replace('\u200c' , ' ')
            string_file = string_file.replace('u200c' , ' ')
            string_file_split = string_file.split('\n')
            title = string_file_split[0]
            price = string_file_split[1]
            price = price.replace(',' , '')
            price = price.replace('تومان' , '')
            price = price.replace(' ' , '')
            amlak = string_file_split[2]
            df_news = df_news.append({'title': title , 'price_t': price , 'amlak': amlak}, ignore_index=True)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")      
    time.sleep(2)
df_news = df_news.drop_duplicates()
df_news = df_news.sort_values( [ 'price_t' ] , ascending = True )
df_news.columns = ['title', 'price_t', 'amlak']
df_news_n = psql.sqldf("select *  from df_news where title like  '%" + str(mahal_name)+ "%'")
df_news_n.to_excel( './divar.xlsx' ,index = False)











