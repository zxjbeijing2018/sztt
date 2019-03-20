# -*- coding:utf-8 -*-
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls'))
]
