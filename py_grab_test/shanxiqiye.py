# import time
# from collections import OrderedDict
# from pprint import pprint

# import pandas as pd
# import re
# from py_grab_test.get_driver import init_driver
from selenium import webdriver
from bs4 import BeautifulSoup
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import requests
# import json
# from lmf.dbv2 import db_write


driver = webdriver.Chrome()


driver.maximize_window()
driver.implicitly_wait(10)
driver.get("http://zjt.shanxi.gov.cn/SXJGPublic/HTML/Enterprise_List")
html = driver.page_source

soup = BeautifulSoup(html,'html.parser')
# print(soup)
# print(soup.select('.dashboard-message>table>tbody#List_Enterprises>tr:nth-child(1)>td:nth-child(2)>a')[0].get_text())
trs = soup.select('.dashboard-message>table>tbody#List_Enterprises>tr')
print(trs)
for tr in trs:
    href = tr.find('a')['href']
    print(href)




