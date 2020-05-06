#coding=utf-8
#包含一些基本操作函数
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
import datetime
from pykeyboard import PyKeyboard
from pymouse import PyMouse
import time
import xlrd

k=PyKeyboard()
m=PyMouse()
driver=webdriver.Chrome()

class Base_():
    def __init__(self):
#         self.driver=webdriver.Chrome()
        pass
    #元素定位
    def get_position(self,method,value,):
        try:
            ele=WebDriverWait(driver,20,0.5).until(lambda x:x.find_element(method,value))
        except Exception:
            #如果元素没有找到，截图
            t=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            driver.get_screenshot_as_file("E:/capture/%s.png"%t)
            #没有找到时，返回一个空值
            return None
        else:
            #找到了就返回正确的元素位置
            return ele
    #打开网址
    def open_(self,url):
        driver.get(url)
        driver.maximize_window()
        driver.implicitly_wait(20)
    #输入框输入英文
    def input_e(self,method,value,data):
        ele = self.get_position(method, value)
        if ele!=None:
            ele.clear()
            ele.click()
            k.type_string(data)
            k.tap_key(k.enter_key)
    #input输入框输入中文,value值是一个css选择器,method只支持css定位；css里面如果有引号则必须使用双引号，否则会出现未知错误
    def input_c(self,method,value,data):
        ele=self.get_position(method, value)
        data=str(data)
        driver.execute_script('document.querySelector(\''+value+'\').value="%s"'%data)
        ele.click()
        k.type_string(' ')
        k.tap_key(k.enter_key)
        ele.click()
        k.tap_key(k.backspace_key)
    #会自动去空格的输入框使用下面的输入方式
    def input_c1(self,method,value,data):
        ele=self.get_position(method,value)
        driver.execute_script('document.querySelector(\''+value+'\').value=\"'+data+'\"')
        ele.click()
        k.type_string(' ')
        k.tap_key(k.enter_key)
    #使用js修改html元素的值
    def change_html(self,dom,value,data):
        if dom=="innerText":
            driver.execute_script('document.querySelector(\''+value+'\').innerText="%s"'%data)
    #元素点击操作
    def click_(self,method,value):
        ele=self.get_position(method,value)
        if ele!=None:
            ele.click()
        else:
            print("没有找到元素")
    #使用js进行元素点击操作,针对不可见元素点击,value只能用css进行定位
    def click_s(self,value):
        try:
            driver.execute_script('document.querySelector(\''+value+'\').click()')
        except Exception:
            print("只能使用css定位，或找不到元素")
    #向下滚动,n表示按多少次down键，x,y用来进行点击使能够滚动的部分获得焦点
    def roll_down(self,n,x=0,y=0,interval=0.5):
        m.click(x,y)
        m.click(x,y)
        time.sleep(1)
        k.tap_key(k.down_key,n,interval)
    #截图功能,pic_name表示图片名，position表示图片存放位置，t=True时表示拼接了时间对图片命名
    def screen_shut(self,pic_name,position,t=True):
        if t:
            t=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            t=''
        try:
            driver.get_screenshot_as_file(position+t+str(pic_name)+'.png')
            print("success")
        except BaseException as msg:
            print(msg)
    #使用js判断页面元素是否存在,存在返回1，不存在返回-1
    def exist_or_not(self,value):
        ex=driver.execute_script('return document.querySelector(\''+value+'\')')
        if ex:
            return 1
        else:
            return -1
    #读取excel文件，返回一个嵌套列表;每行是一个列表
    def read_excel(self,filename,sheetname):
        file=xlrd.open_workbook(filename)
        sheet=file.sheet_by_name(sheetname)
        nr=sheet.nrows
        lis=[]
        for i in range(0,nr):
            list_ = sheet.row_values(i)
            lis.append(list_)
        return lis
    #使用js获取页面元素的文本内容，value是css选择器
    def get_text(self,value):
        txt=driver.execute_script('return document.querySelector(\''+value+'\').innerText')
        return txt
    #使用select寻找元素位置
    def select_by_value(self,method,value,value1):
        ele = self.get_position(method, value)
        s = Select(ele)
        s.select_by_value(value1)
















