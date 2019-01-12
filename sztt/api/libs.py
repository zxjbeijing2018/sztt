# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework import status

from api.models import *


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
                return JsonResponse(response, status=status)
            except Exception as e:
                return HttpResponse('[ERROR] "{0}"'.format(str(e)))
        else:
            return FileResponse(content, status=status)


def get_article_info(_max):
    url_root = "http://jhsjk.people.cn/result/{}?title=&content=&form=0&year=0&submit=%E6%90%9C%E7%B4%A2"
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
            except Exception:
                pass


def get_article(_article_info):
    url = "http://jhsjk.people.cn/article/{}".format(_article_info['id'])
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    content = str(soup.find('div', attrs={'class': 'd2txt clearfix'}))
    try:
        article_obj = article(
            article_id=_article_info['id']
            article_title=_article_info['title']
            article_date=_article_info['date']
            article_content=content
        )
        article_obj.save()
    except Exception:
        pass
