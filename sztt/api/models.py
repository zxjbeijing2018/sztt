from django.db import models


class article(models.Model):
    article_id = models.CharField(max_length=255)
    article_title = models.CharField(max_length=512)
    article_date = models.DateField()
    article_content = models.TextField()
