from selenium import  webdriver
from bs4 import BeautifulSoup
import psycopg2

# 初始化一个网页对象，返回网页内容
def get_html(url):
    # webdriver初始化
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()

    # 打开网页，获取页面信息
    driver.get(url)
    html = driver.page_source
    return html



# 将数据存储到数据库里面
def store(href,database="htest001_db",user="postgres",password="123456",host="127.0.0.1",port="5433",**infos):
    conn = psycopg2.connect(database,user,password,host,port)
    cur = conn.cursor()
    for i in range(len(infos)):
        zz = infos[i].get_text().replace(",", "")
        print(type(zz))
        cur.execute("INSERT INTO henan.qyzz(id, href, zzmc, entname) VALUES ('%i','%s' , '%s', '%s');" % (
        i, href, zz, "a"))
    cur.execute("select * from henan.qyzz;")
    zz = cur.fetchall()
    print(zz)
    print("operation is successful")

# 将数据保存到excel表里

