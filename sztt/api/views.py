# -*- coding:utf-8 -*-
from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.parsers import JSONParser

from api.libs import *


@csrf_exempt
def spider(request):
    if request.method != 'POST':
        return make_response("Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        try:
            if request.POST['authorized'] == '57589':
                for ar in get_article_info(329):
                    get_article(ar)
                return make_response("OK")
        except Exception as e:
            print(e)
            return make_response("Authorization failure", status.HTTP_403_FORBIDDEN)


@csrf_exempt
def get_article(request):
    if request.method != 'GET':
        return make_response("Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        articlelist = []
        try:
            article_obj = article.objects.get(article_id='30523243')
            return make_response(
                {
                    "id": article_obj.article_id,
                    "title": article_obj.article_title,
                    "date": article_obj.article_date,
                    "content": article_obj.article_content.replace('\n', '').replace('\\', '')
                }
            )
        except Exception as e:
            print(e)
            return make_response("Internal Server Error", status.HTTP_500_INTERNAL_SERVER_ERROR)
