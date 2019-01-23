# -*- coding:utf-8 -*-
from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser

from api.libs import *


@csrf_exempt
def spider(request):
    if request.method != 'POST':
        return make_response("Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        try:
            if request.META.get('HTTP_AUTHORIZED') == '57589':
                for ar in get_article_info():
                    get_article(ar)
                return make_response("OK")
            else:
                raise RuntimeError("Authorization failure")
        except Exception as e:
            print(e)
            return make_response("Authorization failure", status.HTTP_403_FORBIDDEN)


@csrf_exempt
def getarticle(request, _id):
    if request.method != 'GET':
        return make_response("Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        try:
            article_obj = article.objects.get(article_id=_id)
            return make_response(
                {
                    "id": article_obj.article_id,
                    "title": article_obj.article_title,
                    "date": article_obj.article_date,
                    "content": article_obj.article_content
                }
            )
        except Exception as e:
            print(e)
            return make_response("Article Not Exist", status.HTTP_404_NOT_FOUND)


@csrf_exempt
def article_list(request):
    if request.method != 'GET':
        return make_response("Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        article_list = []
        try:
            article_objs = article.objects.all()
            for article_obj in article_objs:
                article_list.append(
                    {
                        "id": article_obj.article_id,
                        "title": article_obj.article_title,
                        "date": article_obj.article_date,
                        "author_avatar": article_obj.article_cover
                    }
                )
        except Exception as e:
            print(e)
            return make_response("Article Not Exist", status.HTTP_500_INTERNAL_SERVER_ERROR)
        return make_response(article_list)
