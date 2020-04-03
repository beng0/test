import random
import re

import requests
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

from get_driver import init_driver
from zlsrc.util.etl import est_html, est_meta
import time

def f1(driver, num):
    locator = (By.XPATH, "//ul[@id='info']/li")
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))

    page_temp = driver.find_element_by_xpath("//li[@class='no-active']/a").text
    cnum = re.findall("(\d+)\/",page_temp)[0]

    if int(cnum) != int(num):
        val = driver.find_element_by_xpath("//ul[@id='info']/li[1]/div[@class='title']/a").text

        driver.find_element_by_xpath('//div[@id="jumpDiv"]/input').clear()
        driver.find_element_by_xpath('//div[@id="jumpDiv"]/input').send_keys(num)
        driver.find_element_by_id('jump').click()

        locator = (By.XPATH, '//ul[@id="info"]/li[1]/div[@class="title"]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    data = []
    page = driver.page_source

    body = etree.HTML(page)
    content_list = body.xpath("//ul[@id='info']/li")
    for content in content_list:
        name = content.xpath("./div[@class='title']/a/text()")[0].strip()
        logicId = re.findall("\d+",content.xpath("./@onclick")[0].strip())[0]

        url_temp = 'http://ggzyjy.liaoyang.gov.cn/' + "releaseCms/dynamicArticle.do?siteCode=GGZY&logicId="+logicId+"&selfSiteSiteId=152341388865840&columnLogicId=152341388865850&isWap=0&navigationSiteId=152696583127019"

        ggstart_time = time.strftime('%Y-',time.localtime(int(logicId)//100000 if len(logicId) == 15 else int(logicId)//10000)) + content.xpath("./div[@class='date']/text()")[0]
        temp = [name, ggstart_time, url_temp]
        data.append(temp)

    df = pd.DataFrame(data=data,columns=["name","ggstart_time","href"])
    df["info"] = None
    return df



def work(conp):
    driver=init_driver()
    driver.get("http://www.liaoyang.gov.cn/OpenData/opendata/ggzy/list/PurchaseList1.html")
    result=f1(driver,5)
    db_write(result,'liaoning_liaoyang_ggzy_gg',dbtype="postgresql",conp=conp)


if __name__ == "__main__":
    conp = ["postgres", "since2015", "192.168.1.171", "lichanghua", "public"]
    work(conp)
