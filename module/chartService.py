#-*- coding:utf-8 -*-

from module import OracleDB as odb
from module import MongoDB as mdb
from datetime import datetime
import pandas as pd
import calendar

def createQuery(age, gender, year, month):
    str = {}
    if age != '' :
        age = int(age)
        str["age"] = {"$gte":age, "$lt":age + 10}
    if gender != '' : str["gender"] = gender
    if month != '' :
        year = int(year)
        month = int(month)
        last_day = int(calendar.monthrange(year, month)[1])
        str["createdAt"] = {"$gte":datetime(year, month, 1), "$lt":datetime(year, month, last_day)}
    return str


def inquiryChart(age, gender, year, month):
    str = createQuery(age, gender, year, month)
    curosr = mdb.inquiry.find(str, {"_id":0, "_class":0})

    data = []
    for c in curosr: data.append(list([c['age'], c['createdAt'].month, c['gender'], c['mcate']]))

    name = ['age', 'month', 'gender', 'category']
    df = pd.DataFrame(data, columns=name)
    df2 = df.groupby(['category', 'gender'])['gender'].count().reset_index(name='count')

    male = df2[df2['gender'] == 'male'][['category', 'count']]
    male.index = df2[df2['gender'] == 'male']['category']
    female = df2[df2['gender'] == 'female'][['category', 'count']]
    female.index = df2[df2['gender'] == 'female']['category']

    sql = "SELECT eValue FROM env WHERE eName='category'"
    odb.cursor.execute(sql)
    index = []
    for r in odb.cursor.fetchall():
        index.append(r[0])

    result = pd.DataFrame(index=index)
    result['male'] = male['count']
    result['female'] = female['count']
    result = result.fillna(0)

    return {'label' : index, 'legend' : result.columns, 'data' : result}

def orderChart(age, gender, year, month):
    str = createQuery(age, gender, year, month)
    curosr = mdb.order.find(str, {"_id":0, "_class":0})

    data = []
    for c in curosr: data.append(list([c['age'], c['createdAt'].month, c['gender'], c['mcate']]))

    name = ['age', 'month', 'gender', 'category']
    df = pd.DataFrame(data, columns=name)
    df2 = df.groupby(['category', 'gender'])['gender'].count().reset_index(name='count')

    male = df2[df2['gender'] == 'male'][['category', 'count']]
    male.index = df2[df2['gender'] == 'male']['category']
    female = df2[df2['gender'] == 'female'][['category', 'count']]
    female.index = df2[df2['gender'] == 'female']['category']

    sql = "SELECT eValue FROM env WHERE eName='category'"
    odb.cursor.execute(sql)
    index = []
    for r in odb.cursor.fetchall():
        index.append(r[0])

    result = pd.DataFrame(index=index)
    result['male'] = male['count']
    result['female'] = female['count']
    result = result.fillna(0)

    return {'label' : index, 'legend' : result.columns, 'data' : result}