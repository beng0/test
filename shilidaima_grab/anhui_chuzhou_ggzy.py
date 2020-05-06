import time
from collections import OrderedDict
from pprint import pprint

import pandas as pd
import re
from shilidaima_grab.get_driver import init_driver
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
from lmf.dbv2 import db_write


def f1(driver, num):

    locator = (By.XPATH, '//div[@id="infolist"]/div/table//tr[1]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    cnum = re.findall('Paging=(\d+)',url)[0]
    if int(cnum) != num:
        val = driver.find_element_by_xpath('//div[@id="infolist"]/div/table//tr[1]//a').get_attribute('href')[-60:-30]
        url=re.sub('Paging=\d+','Paging=%s'%num,url)
        driver.get(url)
        # 第二个等待
        locator = (By.XPATH,'//div[@id="infolist"]/div/table//tr[1]//a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []
    html = driver.page_source

    print(html)

    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', id='infolist')
    trs = div.find_all('tr', height=25)

    for tr in trs:
        href = tr.find('td', align='left').a['href']
        name = tr.find('td', align='left').a['title']
        ggstart_time = tr.find('td', align='right').get_text()

        if 'http' not in href:
            href = 'http://ggzy.chuzhou.gov.cn' + href

        tmp = [name, ggstart_time, href]
        print(tmp)
        data.append(tmp)
    df = pd.DataFrame(data=data,columns=["name","ggstart_time","href"])
    df["info"] = None
    return df


def work(conp):
    driver=init_driver()
    driver.get("https://ggzy.chuzhou.gov.cn/Front_jyzx/ShowInfo/ShowSearchInfo.aspx?CategoryNum=002008001001&Eptr3=&datefrom=&dateto=&xiaqu=&zbfs=&Paging=1")
    result=f1(driver,5)
    db_write(result,'anhui_chuzhou_ggzy_gg',dbtype="postgresql",conp=conp)



if __name__ == "__main__":
    conp = ["postgres", "since2015", "192.168.1.171", "lichanghua", "public"]
    work(conp)
