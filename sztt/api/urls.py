from django.urls import path
from api import views as api_views

urlpatterns = [
    path('spider', api_views.spider),
    path('get_article', api_views.article),

]
