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
        for ar in get_article_info(329):
            get_article(ar)
        return make_response("OK")
