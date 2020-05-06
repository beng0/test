#coding=utf-8

from selenium import  webdriver
from bs4 import BeautifulSoup
import psycopg2

# webdriver初始化
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.maximize_window()

# 打开网页，获取页面信息
driver.get("http://hngcjs.hnjs.gov.cn/company/QiyeDetail?id=399994")
html = driver.page_source

# 将页面转换为soup文档
soup = BeautifulSoup(html,"html.parser")

# 获取iframe里的链接并打开
iframe_src = soup.select_one("#newsiframe").attrs["src"]
qyzz_href = "http://hngcjs.hnjs.gov.cn" + iframe_src
r = driver.get(qyzz_href)

# 保存iframe页面信息并转换为soup文档解析
html1 = driver.page_source
soup1 = BeautifulSoup(html1,"html.parser")
qyzzs = soup1.select("tbody>tr:nth-child(4)>td:nth-child(2)>span")

for qyzz in qyzzs:
    print(qyzz.get_text().replace(",",""))

# 将解析后的数据存储到数据库里面
conn = psycopg2.connect(database="htest001_db",user="postgres",password="123456",host="127.0.0.1",port="5433")
cur = conn.cursor()
# cur.execute("create table henan.qyzz(id int,href text,zzmc text,entname text)")
for i in range(len(qyzzs)):
    zz = qyzzs[i].get_text().replace(",","")
    print(type(zz))
    cur.execute("INSERT INTO henan.qyzz(id, href, zzmc, entname) VALUES ('%i','%s' , '%s', '%s');"%(i,qyzz_href,zz,"a"))
cur.execute("select * from henan.qyzz;")
zz = cur.fetchall()
print(zz)
print("operation is successful")

conn.commit()
cur.close()
conn.close()











