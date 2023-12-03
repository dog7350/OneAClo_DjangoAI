#-*- coding:utf-8 -*-

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from module import OracleDB as odb
from module import MongoDB as mdb
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
import time


def initUserData(age, gender, year, month):
    str = {}

    if age != '' : str["age"] = int(age)
    else :
        sql = "SELECT ROUND(AVG(age), 0) FROM memberInfo"
        odb.cursor.execute(sql)
        age = odb.cursor.fetchall()[0][0]
        str["age"] = int(age) / 10 * 10

    if (gender == 'male') : str["gender"] = 1
    else : str["gender"] = 0

    if year != '' or month != '' :
        str['year'] = int(year)
        str['month'] = int(month)
    else :
        str['year'] = int(datetime.today().year)
        str['month'] = int(datetime.today().month)

    return str


def modelInitGbc(data) :
    head = ['cate', 'age', 'gender', 'year', 'month']
    df = pd.DataFrame(data, columns=head)
    df.loc[df['gender'] == 'male', 'gender'] = 1
    df.loc[df['gender'] == 'female', 'gender'] = 0

    attr = ['age', 'gender', 'year', 'month']
    label = 'cate'
    X, y = df[attr], df[label]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    gbc = GradientBoostingClassifier()
    gbc.fit(X_train, y_train)
    print("train : ", gbc.score( X_train, y_train ))
    print("test : ", gbc.score( X_test, y_test ))

    return gbc


def agentSelect(useragent) :
    agent = ""

    if useragent == "Chrome" : agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
    elif useragent == "Firefox" : agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0"
    elif useragent == "Edge" : agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    elif useragent == "Safari" : agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
    elif useragent == "Mozilla" : agent = "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"
    elif useragent == "Opera" : agent = "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2"

    return agent


def inquiryAnalysis(age, gender, year, month) :
    user = initUserData(age, gender, year, month)

    curosr = mdb.inquiry.find({}, {"_id":0, "pno":0, "bcate":0, "scate":0, "userid":0, "address":0, "_class":0})
    data = []
    for c in curosr : data.append(list([c['mcate'], c['age'], c['gender'], c['createdAt'].year, c['createdAt'].month]))

    if (len(data) > 10) : result = modelInitGbc(data).predict([[ user['age'], user['gender'], user['year'], user['month'] ]])
    else : result = [['데이터가 너무 적습니다']]
    time.sleep(2)

    return {"category" : result[0], "age" : user["age"]}

def orderAnalysis(age, gender, year, month) :
    user = initUserData(age, gender, year, month)

    curosr = mdb.order.find({}, {"_id":0, "pno":0, "bcate":0, "scate":0, "count":0, "_class":0})
    data = []
    for c in curosr : data.append(list([c['mcate'], c['age'], c['gender'], c['createdAt'].year, c['createdAt'].month]))

    if (len(data) > 10) : result = modelInitGbc(data).predict([[ user['age'], user['gender'], user['year'], user['month'] ]])
    else : result = [['데이터가 너무 적습니다']]
    time.sleep(2)

    return {"category" : result[0], "age" : user["age"]}

def webCrawling(age, gender, category, useragent) :
    data = {}
    agent = agentSelect(useragent)
    url = "http://www.google.co.kr/search?q=" + age + "대+" + gender + "+최신+" + category + "+추천"
    headers = {'User-Agent' : agent}

    resp = requests.get(url, headers=headers)

    if str(resp.status_code) == '200' :
        soup = BeautifulSoup(resp.text, "html.parser")
        time.sleep(5)
        result = soup.select("div.Gor6zc.JtzP6")

        list = []
        for r in result :
            list.append(str(r))

        data = {"list" : list}
    else :
        print("Error : " + str(resp.status_code))
        print("Error : " + str(resp.headers))
        print("Error : " + str(resp.url))
        data = {"code" : str(resp.status_code), "headers" : str(resp.headers), "url" : str(resp.url)}

    return data