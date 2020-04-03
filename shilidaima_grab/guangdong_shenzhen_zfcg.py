import pandas as pd
import re

from lmf.dbv2 import db_write
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys
import time

from get_driver import init_driver
from zlsrc.util.etl import est_html, est_meta, add_info, est_meta_large, load_page_wait

sys.setrecursionlimit(4000)


def f1(driver, num):
    locator = (By.XPATH, "//tbody[@class='tableBody']/tr[1]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//select[@name='__ec_pages']/option[@selected='selected']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        cnum = int(str)
    except:
        cnum = 1

    if num != cnum:
        val = driver.find_element_by_xpath("//tbody[@class='tableBody']/tr[1]/td/a").get_attribute('href')[-12:]

        selector = Select(driver.find_element_by_xpath("//select[@name='__ec_pages']"))
        selector.select_by_value('{}'.format(num))

        locator = (By.XPATH, "//tbody[@class='tableBody']/tr[1]/td/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    div = soup.find("tbody", class_="tableBody")
    trs = div.find_all("tr")
    data = []
    for tr in trs:
        a = tr.find('a')
        title = a.text.strip()
        td = tr.find_all('td')[-1].text.strip()
        href = a['href'].strip()
        id = re.findall(r'id=(.*)', href)[0]
        link = 'http://www.szzfcg.cn/portal/documentView.do?method=view&id=' + id
        info = {}
        if tr.find_all('td')[-2]:
            lx = tr.find_all('td')[-2].text.strip()
            if lx: info['lx'] = lx
        if info:
            info = json.dumps(info, ensure_ascii=False)
        else:
            info = None
        tmp = [title, td, link, info]
        print(tmp)
        data.append(tmp)
    df = pd.DataFrame(data=data, columns=["name", "ggstart_time", "href", "info"])
    return df


def work(conp):
    driver = init_driver()
    driver.get("http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660&agencyType=1")
    result = f1(driver, 5)
    db_write(result, 'guangdong_shenzhen_zfcg_gg', dbtype="postgresql", conp=conp)


if __name__ == "__main__":
    conp = ["postgres", "since2015", "192.168.1.171", "lichanghua", "public"]
    work(conp)

