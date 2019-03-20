# -*- coding:utf-8 -*-
import json
import math

import requests
from bs4 import BeautifulSoup
from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework import status

from .models import *


def make_response(content='', status=status.HTTP_200_OK, typed='application/json', cookie=None):
    '''
        typed = 'text/*' return HttpResponse(content)\n
        typed = 'application/json' return JsonResponse(content)\n
        typed = 'application/*' return FileResponse(content)\n
    '''
    if typed.split('/')[0] == 'text':
        return HttpResponse(content, status)
    if typed.split('/')[0] == 'application':
        if typed.split('/')[-1] == 'json':
            response = dict()
            response['code'] = status
            if isinstance(content, (str, bytes, bytearray)):
                try:
                    response['data'] = json.loads(content)
                except Exception:
                    response['data'] = content
            elif isinstance(content, (dict, list, tuple)):
                response['data'] = content
            else:
                response['data'] = 'NUll'
            try:
                return JsonResponse(response, status=status, json_dumps_params={'ensure_ascii': False})
            except Exception as e:
                return HttpResponse('[ERROR] "{0}"'.format(str(e)))
        else:
            return FileResponse(content, status=status)


def get_article_info():
    
    def find_number(_str):
        import re
        res = re.findall(r'\d+', _str)
        return int(res[0]) if res else None

    url_root = "http://jhsjk.people.cn/result/{}?title=&content=&form=0&year=0&submit=%E6%90%9C%E7%B4%A2"
    pn_url = url_root.format('')
    pn_response = requests.get(pn_url, timeout=5)
    pn_soup = BeautifulSoup(pn_response.text, "lxml")
    pn_div = pn_soup.find('div', attrs={'class': 'fr'})
    article_count = find_number(pn_div.h1.get_text())
    _max = math.ceil(article_count / 24)

    for i in range(1, _max+1):
        url = url_root.format(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        for li in soup.find('ul', attrs={'class': 'list_14 p1_2 clearfix'}):
            try:
                yield {
                    'id': li.a['href'].split('/')[-1],
                    'title': li.a.string,
                    'date': li.get_text().strip()[-11:-1]
                }
            except Exception as e:
                pass


def get_article(_article_info):
    url = "http://jhsjk.people.cn/article/{}".format(_article_info['id'])
    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        print(f"TimeOut:{url}")
        return
    soup = BeautifulSoup(response.text, "lxml")

    # 文章全部信息
    wcontent = soup.find('div', attrs={'class': 'd2txt clearfix'})

    # 标题信息
    subtitle = wcontent.find('h1')

    # 来源信息
    source = wcontent.find('div', attrs={'class': 'd2txt_1 clearfix'})
    source = source.string.split(' ')[0].split('：')[-1]
    source = source if source else 'NULL'

    # 文章主体
    content = wcontent.find('div', attrs={'class': 'd2txt_con clearfix'})

    # 编辑
    editor = wcontent.find('div', attrs={'class': 'editor clearfix'})
    editor = editor.string[1:-1].strip().split('：')[-1]
    editor = editor if editor else 'NULL'

    # 提取文章第一张图片作为封面，如果没有为 NULL
    cover = content.find('img')
    try:
        cover = str(cover['src'])
    except Exception:
        cover = 'NULL'

    # 删除被居中的文字
    for match in content.findAll('p', attrs={'style': 'text-indent: 2em; text-align: center;'}):
        match.decompose()

    # 删除所有的表格标签
    tabletags = ["table", "tbody", "tr", "td", "th"]
    for ttag in tabletags:
        for match in content.findAll(ttag):
            match.replaceWithChildren()

    # 删除所有的 h 标签
    htags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    for htag in htags:
        for match in content.findAll(htag):
            match.replaceWithChildren()

    # 删除所有的 div 标签
    for match in content.findAll('div'):
        match.replaceWithChildren()

    #删除所有的标签属性
    del content["class"]
    for tag in content():
        for attribute in ["class", "id", "name", "style", "align", "width", "height"]:
            del tag[attribute]

    # 删除文章中所有的图片
    for match in content.findAll('img'):
        match.decompose()

    # 删除所有的 a 标签
    for match in content.findAll('a'):
        match.replaceWithChildren()

    # 删除所有的粗体
    for match in content.findAll('strong'):
        match.replaceWithChildren()

    for match in content.findAll('p'):
        if not match.string:
            match.replaceWithChildren()

    # 去除所有的换行符
    content = str(content).replace('\n', '')

    try:
        article_obj = article(
            article_id=_article_info['id'],
            article_title=_article_info['title'],
            article_date=_article_info['date'],
            article_content=content,
            article_source=source,
            article_editor=editor,
            article_cover=cover,
            article_category=category.objects.get(category_id=0)
        )
        article_obj.save()
        return
    except Exception:
        pass


def get_category():
    cat_dict = {}
    try:
        category_obj_list = category.objects.all()
        for cat in category_obj_list:
            cat_dict[cat.category_id] = cat.category_name
    except Exception as e:
        print(e)
    return cat_dict
