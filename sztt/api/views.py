# -*- coding:utf-8 -*-
from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from .libs import *
from .tasks import run_spider


@csrf_exempt
def spider(request):
    if request.method != 'POST':
        return make_response("Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        try:
            if request.META.get('HTTP_AUTHORIZED') == 'wyl':
                run_spider.delay()
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
                    "source": article_obj.article_source,
                    "content": article_obj.article_content,
                    "category": {
                        "id": article_obj.article_category.category_id,
                        "display_name": article_obj.article_category.category_name
                    }
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
            cat = request.GET.get('category_id', default=0)
            limit = request.GET.get('limit', default=50)
            article_objs = article.objects.filter(
                article_category=cat).order_by('-article_date')[:int(limit)]
            for article_obj in article_objs:
                article_list.append(
                    {
                        "id": article_obj.article_id,
                        "title": article_obj.article_title,
                        "source": article_obj.article_source,
                        "date": article_obj.article_date,
                        "author_avatar": article_obj.article_cover,
                        "category": {
                            "id": article_obj.article_category.category_id,
                            "display_name": article_obj.article_category.category_name
                        }
                    }
                )
        except Exception as e:
            print(e)
            return make_response("Article Not Exist", status.HTTP_500_INTERNAL_SERVER_ERROR)
        return make_response(article_list)


@csrf_exempt
def add_category(request):
    if request.method != 'POST':
        return make_response("Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        try:
            cat_id = request.POST['category_id']
            cat_name = request.POST['category_name']
        except Exception as e:
            print(e)
            return make_response("Lack of necessary information", status.HTTP_406_NOT_ACCEPTABLE)
        try:
            category_obj = category(
                category_id=cat_id,
                category_name=cat_name
            )
            category_obj.save()
        except Exception as e:
            print(e)
            return make_response("Failed to create category", status.HTTP_500_INTERNAL_SERVER_ERROR)
        return make_response("OK")


@csrf_exempt
def category_list(request):
    if request.method != 'GET':
        return make_response("Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        category_obj = category.objects.all()
        catdict = []
        for cat in category_obj:
            catdict.append(
                {
                    'id': cat.category_id,
                    'name': cat.category_name
                }
            )
        return make_response(catdict, status.HTTP_200_OK)
