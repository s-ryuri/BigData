import os
import re
import warnings
from time import sleep
import pandas as pd
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select
import threading
from html_table_parser import parser_functions as parser

try:
    shutil.rmtree(r"c:\chrometemp")  #쿠키와 캐쉬파일 삭제
    #일단 이걸 안해주면 로그인된 상태로 홈페이지가 뜨는 경우가 있어서 코드가 안 먹힘
except FileNotFoundError:
    pass

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222") #디버거 크롬을 하기위해서 옵션을 넣어줌

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0] # 크롬의 버전을 넣어줌
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
result = pd.DataFrame()

driver.implicitly_wait(10)

driver.maximize_window() # 창 최대크기로


time.sleep(0.001)
driver.switch_to.frame('disp')
driver.switch_to.frame('all')
time.sleep(0.001)
Daegu = driver.find_element_by_xpath('//*[@id="p143"]/a/img').click()
time.sleep(0.001)
driver.switch_to.frame('sub')
Daegu_west = driver.find_element_by_xpath('//*[@id="i846"]/a/img').click() 
time.sleep(0.001)
driver.switch_to.default_content()
time.sleep(1)
day = driver.find_element_by_xpath('//*[@id="datecal2"]').clear() #날짜 초기화하고
time.sleep(0.8)
day2 = driver.find_element_by_xpath('//*[@id="datecal2"]').send_keys('')
time.sleep(0.5)

time.sleep(0.5)
select_button = driver.find_element_by_xpath('//*[@id="frm"]/table/tbody/tr/td[2]/input').click()

cnt = 0
import re
while True:
    driver.switch_to.frame('disp')
    time.sleep(0.1)
    driver.switch_to.frame('body')
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    temp = soup.select('table')
    p = parser.make2d(temp[1])
    df = pd.DataFrame(p[1:],columns =p[0])
    result = pd.concat([result,df])
    print(result)
    driver.switch_to.default_content()
    driver.switch_to.frame('menu')
    min60 = driver.find_element_by_xpath('//*[@id="area00"]/li[2]/a')
    driver.execute_script("arguments[0].click();", min60)
    time.sleep(0.02)
    driver.switch_to.default_content()
    print(cnt)
    cnt += 1

result.to_csv('helloworld.csv',index = False, encoding="utf-8-sig")
