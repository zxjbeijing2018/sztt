# -*- coding:utf-8 -*-
from django.urls import path
from api import views as api_views

urlpatterns = [
    path('spider', api_views.spider),
    path('article/<_id>', api_views.getarticle),

]
