# -*- coding:utf-8 -*-
from django.urls import path
from api import views as api_views

urlpatterns = [
    path('spider', api_views.spider),
    path('article/<_id>', api_views.getarticle),
    path('article/list', api_views.article_list),
    path('category/add', api_views.add_category),
    path('category/list', api_views.category_list),
]
