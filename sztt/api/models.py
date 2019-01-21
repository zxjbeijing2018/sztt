# -*- coding:utf-8 -*-
from django.db import models


class article(models.Model):
    article_id = models.CharField(max_length=255, primary_key=True)
    article_title = models.CharField(max_length=512)
    article_date = models.DateField()
    article_cover = models.CharField(max_length=4096)
    article_content = models.TextField()
