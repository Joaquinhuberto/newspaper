
from django.shortcuts import render_to_response

from newspaper.settings import NUM_ITEMS_PAG
from newspaper.news.models import News


def news_list(request):
    news_published = News.objects.news_published()[:NUM_ITEMS_PAG]
    news_next_published = News.objects.news_next_published()[:NUM_ITEMS_PAG]
    return render_to_response("news/news_list.html",
                              {'news_published': news_published,
                               "news_next_published": news_next_published})
