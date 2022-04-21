from datetime import datetime
from django.shortcuts import render, redirect
from stocks.models import StockTradeInfo, Stock

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
import os
import requests
import re
import pandas as pd
import FinanceDataReader as fdr

from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

from urllib import parse 
from ast import literal_eval
import requests

from datetime import date, datetime

# chrome = webdriver.Chrome()

def get_sise(code, start_time, end_time, time_from='day') :
    get_param = { 'symbol':code, 'requestType':1, 'startTime':start_time,
                 'endTime':end_time, 'timeframe':time_from }
    get_param = parse.urlencode(get_param) 
    url="https://api.finance.naver.com/siseJson.naver?%s"%(get_param) 
    response = requests.get(url) 
    return literal_eval(response.text.strip()) 

def get_stock_name(number):
    chrome.get("https://finance.naver.com/item/main.nhn?code="+number+"#")
    market = chrome.find_element_by_class_name("wrap_company")
    company_name = market.text.split("\n")[0]
    return company_name

def get_stock_name_and_number(start=10, end=30): # 주식 명, 종목번호 가져오기(return = [[이름, 번호]])
    out = []
    for i in range(start,end+1):
        j = '{:06d}'.format(i)
        chrome.get("https://finance.naver.com/item/main.nhn?code="+j+"#")
        try:
            market = chrome.find_element_by_class_name("wrap_company")
            company_name = market.text.split("\n")[0]
            company_number = market.text.split("\n")[1]
            out.append([company_name,company_number]) # name, stock_number array return
        except:
            pass
    return out

def get_trade_info(number):
    num = '{:06d}'.format(int(number))
    chrome.get("https://finance.naver.com/item/sise.nhn?code="+num+"#")
    day = chrome.find_element_by_name("day")
    day_src = day.get_attribute("src").replace("time","day")
    t = []
    for i in range(1,11):
        chrome.get(day_src + "&page=" +str(i))
#         numbe = chrome.find_elements_by_class_name("num")
        tb = chrome.find_element_by_class_name("type2")
        tbt = tb.text
        tbt = tbt.replace(",", "")
        tbtx = tbt.split("\n")
        if( i != 1 ):
            tbtx = tbtx[1:]
        for j in range(0, len(tbtx)):
            tmp = [tbtx[j].split(" ")]
            t = t + tmp
    t_pd = pd.DataFrame(t[1:], columns=t[0])
    # pandas
    high_prices = pd.to_numeric(t_pd['고가'].values)
    low_prices = pd.to_numeric(t_pd['저가'].values)
    print(high_prices)
    print(low_prices)
    if(any(high_prices) == 0):
        return None, 0
    mid_prices = (high_prices + low_prices) / 2
    mid_prices_rev = mid_prices[-1::-1]
    mid_prices_rev_norm = mid_prices_rev/mid_prices_rev[0] - 1
    return np.array(mid_prices_rev_norm), mid_prices_rev[0]

def get_results(data, start=0, ends= 5):
    predicted_price = []
    how_much_up = []
    b_clone = []
    for j in data[start:ends]:
#         print(j)
        try:
            tmp, tmp_ = get_trade_info(j)
            if tmp == None:
                continue
        except:
            print(j + "can't be predicted")
            pass
        b_clone.append(j)
        tmp_np = np.reshape(np.array(tmp),[1,100,1])
        tmp2 = model.predict(tmp_np)
        result = tmp2 - tmp[-1]
        predicted_price.append(tmp2)
        how_much_up.append(result)
    return b_clone, predicted_price, how_much_up

def get_data():
    a_ =[]
    b=[]
    kospi_cd = fdr.StockListing('KOSPI')
    kosdaq_cd = fdr.StockListing('KOSDAQ')
    kosdaq_cd.dropna(axis=0, inplace=True)
    kospi_cd.dropna(axis=0, inplace=True)
    kospi_re = kospi_cd.reset_index(drop=True)
    kosdaq_re = kosdaq_cd.reset_index(drop=True)
    idx1 = np.where(kospi_re['Sector'] == '의약품 제조업')
    idx2 = np.where(kospi_re['Sector'] == '의료용품 및 기타 의약 관련제품 제조업')
    idx3 = np.where(kospi_re['Sector'] == '기초 의약물질 및 생물학적 제제 제조업')
    idx4 = np.where(kospi_re['Sector'] == '의료용 기기 제조업')
    idx5 = np.where(kospi_re['Sector'] == '자연과학 및 공학 연구개발업')
    kospi_re.drop(idx1[0], axis=0, inplace=True)
    kospi_re.drop(idx2[0], axis=0, inplace=True)
    kospi_re.drop(idx3[0], axis=0, inplace=True)
    kospi_re.drop(idx4[0], axis=0, inplace=True)
    kospi_re.drop(idx5[0], axis=0, inplace=True)
    kospi_re2 = kospi_re.reset_index(drop=True)
    
    idx1 = np.where(kosdaq_re['Sector'] == '의약품 제조업')
    idx2 = np.where(kosdaq_re['Sector'] == '의료용품 및 기타 의약 관련제품 제조업')
    idx3 = np.where(kosdaq_re['Sector'] == '기초 의약물질 및 생물학적 제제 제조업')
    idx4 = np.where(kosdaq_re['Sector'] == '의료용 기기 제조업')
    idx5 = np.where(kosdaq_re['Sector'] == '자연과학 및 공학 연구개발업')
    kosdaq_re.drop(idx1[0], axis=0, inplace=True)
    kosdaq_re.drop(idx2[0], axis=0, inplace=True)
    kosdaq_re.drop(idx3[0], axis=0, inplace=True)
    kosdaq_re.drop(idx4[0], axis=0, inplace=True)
    kosdaq_re.drop(idx5[0], axis=0, inplace=True)
    kosdaq_re2 = kosdaq_re.reset_index(drop=True)
    
    a_re = kospi_re2['Symbol']
    b_re =  kospi_re2['Name']
    a_red = kosdaq_re2['Symbol']
    b_red = kosdaq_re2['Name']
    a_re = a_re.reset_index(drop=True)
    b_re = b_re.reset_index(drop=True)
    rr = re.compile('AJ.*|ARIRANG.*|NHF.*|NHG.*|SMART .*|미래F.*|미래G.*|이지스.*|한국F.*|한국G.*|하나대체.*|신한F.*|KOSEF.*|KODEX.*|.*선물.*|HANARO.*|KB.*|KINDEX.*|QV.*|TIGER.*|TRUE.*|대신.*|마이티.*|미래에셋.*|삼성 .*|신한 .*|')
#     c = []

    c=[]
    d=[]
    for i in range(len(b_re)):
#     for i in range(int(len(b_re)/10)):    ### for test
        tmp = rr.findall(b_re[i])
        if tmp[0] == '':
            a_.append(a_re[i])
            c.append(b_re[i])
    for i in range(len(b_red)):
        tmp = rr.findall(b_red[i])
        if tmp[0] == '':
            c.append(a_red[i])
    a_n = np.array(a_)
    ree = re.compile("[0-9]{6}")
    for i in c:
        if len(i) == 6:
            if not ree.findall(i) == []:
                b.append(ree.findall(i)[0])#+".KQ")
    for i in a_n:
        if len(i) == 6:
            if not ree.findall(i) == []:
                b.append(ree.findall(i)[0])#+".KS")
    
    return b
# Create your views here.


def stock_list(request):
    
    return render(request, 'stock_list.html')
    # pass

def make_db(request):
    
    st2_data = get_data()
    
    seq_len = 100
    sequence_length = seq_len + 1
    result = []

    today = date.today().isoformat().replace('-','')

    for i in st2_data:
        comp_num = i[:6]
        comp_name = get_stock_name(comp_num)
        try:
            a = Stock.objects.get(stock_number = comp_num)
            b = StockTradeInfo(stock_number = comp_num)
        except:
            data = pd.DataFrame(get_sise(comp_num, '20220301', today, 'day'))
            data = data.dropna(axis=0)
            # data = data[-100:]

            ns = Stock(
                stock_name = comp_name,
                stock_number = comp_num,
            )
            ns.save()
    
            for j in range(len(data)):
                try:
                    hi = data.iloc[j, 2]
                    lo = data.iloc[j, 3]
                    ed = data.iloc[j, 4]
                    vol = data.iloc[j, 5]
                    md = (hi + lo + 3*ed) / 5
                    cur_date = datetime.strptime(data.iloc[j,0], "%Y%m%d").date()
                    
                    newstock = StockTradeInfo(
                        stock_number = Stock.objects.get(stock_number = comp_num),
                        price_dttm = cur_date,
                        high_price = hi,
                        middle_price = md, 
                        low_price = lo,
                        end_price = ed,
                        volume = vol,
                    )
                    newstock.save()
                except:
                    pass
    
    chrome.quit()
    return redirect('/home/')
    
    