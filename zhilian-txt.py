#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urlencode
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
from config import *
import time
from itertools import product
import csv,codecs
import sys

def download(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    response = requests.get(url, headers=headers)
    return response.text


def get_content(html):
    # 记录保存日期
    date = datetime.now().date()
    date = datetime.strftime(date, '%Y-%m-%d')  # 转变成str

    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    data_main = body.find('div', {'class': 'newlist_list_content'})

    if data_main:
        tables = data_main.find_all('table')

        zw_list = []
        for i, table_info in enumerate(tables):
            if i == 0:
                continue
            temp = []
            tds = table_info.find('tr').find_all('td')
            zwmc = tds[0].find('a').get_text()  # 职位名称
            zw_link = tds[0].find('a').get('href')  # 职位链接
            fkl = tds[1].find('span').get_text()  # 反馈率
            gsmc = tds[2].find('a').get_text()  # 公司名称
            zwyx = tds[3].get_text()  # 职位月薪
            gzdd = tds[4].get_text()  # 工作地点
            gbsj = tds[5].find('span').get_text()  # 发布日期

            tr_brief = table_info.find('tr', {'class': 'newlist_tr_detail'})
            # 招聘信息的简介
            brief = tr_brief.find('li', {'class': 'newlist_deatil_last'}).get_text()

            # 用生成器获取信息
            temp.append(zwmc)
            temp.append(fkl)
            temp.append(gsmc)
            temp.append(zwyx)
            temp.append(gzdd)
            temp.append(gbsj)
            temp.append(brief)
            temp.append(zw_link)

            zw_list.append(temp)
        return zw_list

def main(args_jl_p):
    basic_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?'

    for keyword in KEYWORDS:
        paras = {'jl': args_jl_p[0],
                 'kw': keyword,
                 'p': args_jl_p[1]
                 }
        url = basic_url + urlencode(paras)
        # print(url)
        html = download(url)
        # print(html)
        if html:
            data = get_content(html)
            for item in data:
                print(item)
                write_data(item, "zhilian.txt")

def write_data(item, name):
    filename = name
    with open('zhilian.txt', 'a+', newline='', encoding='utf-8') as f:
        f=codecs.open('zhilian.txt','a+','utf_8_sig')
        f.writelines(item)
        f.writelines('&')
        f.writelines('\r\n')
        f.close()

if __name__ == '__main__':
    start = time.time()
    number_list = list(range(TOTAL_PAGE_NUMBER))
    args = product(ADDRESS, number_list)  # 生成一个可迭代对象
    pool = Pool()
    pool.map(main, args)  # 多进程运行
    end = time.time()
    print('Finished, task runs %s seconds.' % (end - start))







