from pprint import pprint

from selenium import webdriver
import time, math
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from threading import Semaphore
from lmf.dbv2 import db_write
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lmfscrap.fake_useragent import UserAgent
import random
import json

ua = UserAgent()
sema = Semaphore()


def init_driver(ip=False, headless=False, image_show=1, pageloadtimeout=60, pageloadstrategy="normal"):
    chrome_option = webdriver.ChromeOptions()
    if ip:
        ip = get_ip()
        chrome_option.add_argument("--proxy-server=http://%s" % (ip))

    if headless:
        chrome_option.add_argument("--headless")
        chrome_option.add_argument("--no-sandbox")
        chrome_option.add_argument('--disable-gpu')

    prefs = {
        'profile.default_content_setting_values': {'images': image_show, }
    }

    chrome_option.add_experimental_option("prefs", prefs)
    chrome_option.add_argument('--start-maximized')
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = pageloadstrategy
    args = {"desired_capabilities": caps, "chrome_options": chrome_option}
    driver = webdriver.Chrome(**args)

    driver.set_page_load_timeout(pageloadtimeout)

    return driver


def get_ip():
    ###5鍒嗛挓
    # get_ip_url="http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&groupid=0&qty=1&time=101&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=&usertype=2"
    ###1鍒嗛挓
    get_ip_url = "http://zhulong.v4.dailiyun.com/query.txt?key=NPACB534AB&word=&count=1&rand=false&detail=false"
    ###1-5鍒嗛挓
    # get_ip_url="http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&groupid=0&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=&usertype=2"
    # print(self.get_ip_url)
    # get_ip_url="http://192.168.1.170/random"

    sema.acquire()
    i = 3
    try:
        url = get_ip_url
        r = requests.get(url, timeout=40, headers={'User-Agent': ua.random})
        time.sleep(1)
        ip = r.text
        while re.match("[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,5}", ip) is None and i > 0:
            time.sleep(3 - i)
            i -= 1
            url = get_ip_url
            r = requests.get(url, timeout=40, headers={'User-Agent': ua.random})
            time.sleep(1)
            ip = r.text

    except:
        ip = {}
    finally:
        sema.release()

    return ip.strip()