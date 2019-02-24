from celery.decorators import task

from .libs import get_article, get_article_info


@task
def run_spider():
    for ar in get_article_info():
        get_article(ar)
    print("Done")
