import json
import re
import time
import traceback

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lmf.dbv2 import db_command, db_query, db_write
import pandas as pd
from threading import Semaphore
from datetime import datetime
import random
from queue import Queue
from threading import Thread

from bs4 import BeautifulSoup
# from login import get_ip
# from login import get_driver

sema = Semaphore()


def get_parames(conp, total=100):
    user, passwd, host, dbname, schema = conp
    sql1 = '''select qymc,biaoshitong from "%s"."jianshetong_exist_zz_tran"
EXCEPT select qymc,bst_zzcode from "%s"."jianshetong_biaoshitong_result" limit %s''' % (schema, schema, total)
    parames = db_query(sql1, dbtype="postgresql", conp=conp).values.tolist()

    return parames


def get_data(qymc, zzcode,conp):
    sql = """SELECT zzcode FROM "public"."biaoshitong_exist_zz" where  entname = '%s';""" % qymc
    zzcode_list = db_query(sql, dbtype="postgresql", conp=conp)['zzcode'].tolist()

    if zzcode in zzcode_list:
        return 1
    return 0


def work(conp):

    data = []
    parames = get_parames(conp)

    for parame in parames:
        time.sleep(0.1)
        qymc = parame[0]
        zzcode = parame[1]
        result = get_data(qymc, zzcode,conp)
        tmp = [qymc, zzcode, result]
        print(tmp)
        data.append(tmp)
    df = pd.DataFrame(data=data, columns=["qymc", "bst_zzcode", "result"])
    db_write(df, "jianshetong_biaoshitong_result", dbtype='postgresql', conp=conp, if_exists='append')


if __name__ == '__main__':
    conp = ["postgres", "since2015", "192.168.1.171", "jianshetong", "public"]
    work(conp)
