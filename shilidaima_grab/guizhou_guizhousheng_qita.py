import re
import time

from lmf.dbv2 import db_write
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

from get_driver import init_driver
from zlsrc.util.etl import est_meta, est_html, add_info,load_page_wait


def f1(driver, num):
    locator = (By.XPATH, '//div[@class="content_right fr"]//table[contains(@id,"p")]//tr[2]//a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, '//li[@class="page active"]/a')
    cnum=WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    if int(cnum) != num:
        val = driver.find_element_by_xpath('//div[@class="content_right fr"]//table[contains(@id,"p")]//tr[2]//a').get_attribute('href')[-15:]

        driver.execute_script("""(function toPage(page){
        	$("#currentPage").attr("value",page);
        	$("#queryForm").submit();
        })(%s)"""%num)
        time.sleep(0.5) ## 爬取太快了

        locator = (By.XPATH, '//div[@class="content_right fr"]//table[contains(@id,"p")]//tr[2]//a[not(contains(@href,"{}"))]'.format(val))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find('div', class_='content_right fr').find('table',id=re.compile('p')).find_all('tr')[1:]

    for tr in trs:
        tds=tr.find_all('td')
        href = tr.find('a')['href']
        name = tr.find('a').get_text(strip=True)
        ggstart_time = tds[-1].get_text(strip=True)
        zhaobiaoren = tds[-2].get_text(strip=True)
        bh = tds[-3].get_text(strip=True)
        info=json.dumps({'bh':bh,'zhaobiaoren':zhaobiaoren},ensure_ascii=False)
        if 'http' not in href:
            href='http://www.e-qyzc.com'+href

        tmp = [name, ggstart_time, href,info]
        print(tmp)
        data.append(tmp)
    df = pd.DataFrame(data=data,columns=["name","ggstart_time","href","info"])
    # df['info']=None
    return df




def work(conp):
    driver=init_driver()
    driver.get("http://www.e-qyzc.com/gg/ggList")
    result=f1(driver,5)
    db_write(result,'guizhou_guizhousheng_qita_gg',dbtype="postgresql",conp=conp)


if __name__ == "__main__":
    conp = ["postgres", "since2015", "192.168.1.171", "lichanghua", "public"]
    work(conp)

