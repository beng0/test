#coding=utf-8

from py_grab_test.selenium_base import  *
from py_grab_test.base import *
from selenium.webdriver.support.select import Select

se = Base_()

se.open_("http://hngcjs.hnjs.gov.cn/company/qiyeListMaster")
driver.switch_to_frame("newsiframe")
# ele = se.get_position("css selector","select#CretType")
#
# s = Select(ele)
# s.select_by_value("1")
se.select_by_value("css selector","select#CretType","1")
se.click_("name","ctl09")
