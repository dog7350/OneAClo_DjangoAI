#-*- coding:utf-8 -*-

from module import OracleDB as odb
import numpy as np
import pandas as pd


def memberAgeGender():
    sql = "SELECT COUNT(*) count, age, gender FROM (SELECT CASE WHEN age < 20 THEN '10' WHEN age BETWEEN 20 AND 29 THEN '20' WHEN age BETWEEN 30 AND 39 THEN '30' WHEN age BETWEEN 40 AND 49 THEN '40' WHEN age BETWEEN 50 AND 59 THEN '50' WHEN age BETWEEN 60 AND 69 THEN '60' WHEN age BETWEEN 70 AND 79 THEN '70' WHEN age BETWEEN 80 AND 89 THEN '80' WHEN age BETWEEN 90 AND 99 THEN '90' WHEN age >= 100 THEN '100' END AS age, gender FROM memberInfo) GROUP BY gender, age"
    odb.cursor.execute(sql)

    data = odb.cursor.fetchall()
    name = ['count', 'age', 'gender']
    df = pd.DataFrame(data, columns=name)

    male = df[df['gender'] == 'male'][['count']]
    male.index = df[df['gender'] == 'male']['age']
    female = df[df['gender'] == 'female'][['count']]
    female.index = df[df['gender'] == 'female']['age']

    index = ['10', '20', '30', '40', '50', '60', '70', '80', '90']
    result = pd.DataFrame(index=index)
    result['male'] = male
    result['female'] = female
    result = result.fillna(0)

    returns = {'label' : result.index, 'legend' : result.columns, 'data' : result}

    return returns

def memberAddress():
    sql = "SELECT COUNT(*) count, area FROM (SELECT SUBSTR(address, 1, INSTR(address, ' ')) area FROM memberInfo) GROUP BY area"
    odb.cursor.execute(sql)

    data = odb.cursor.fetchall()
    name = ['count', 'area']
    df = pd.DataFrame(data, columns=name)

    area = df[['count']]
    area.index = df['area']

    returns = {'label' : area.index, 'data' : area}

    return returns