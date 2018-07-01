from datetime import datetime


from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from newspaper.news.forms import NewsForm
from newspaper.news.models import News


def news_list(request):
    news_published = News.objects.news_published()
    paginator = Paginator(news_published, settings.NUM_ITEMS_PAG)
    page_default = 1
    page_published = request.GET.get('page', page_default)
    try:
        news_published = paginator.page(page_published)
    except PageNotAnInteger:
        news_published = paginator.page(page_default)
    except EmptyPage:
        news_published = paginator.page(paginator.num_pages)

    news_next_published = News.objects.news_next_published()
    return render_to_response("news/news_list.html",
                              {'news_published': news_published,
                               "news_next_published": news_next_published},
                              context_instance=RequestContext(request))


def news_add(request):
    data = None
    if request.method == 'POST':
        data = request.POST
    initial = {'publish_date': datetime.now()}
    # if 'title' in request.GET:
        # initial['title'] = request.GET['title']
    news_form = NewsForm(data=data,
                         initial=initial)
    if news_form.is_valid():
        news_form.save()
        return HttpResponseRedirect(reverse('news_list'))
    return render_to_response('news/news_add.html',
                              {'news_form': news_form},
                              context_instance=RequestContext(request))


def news_edit(request, newsitem_pk):
    data = None
    if request.method == 'POST':
        data = request.POST
    news_item = get_object_or_404(News, pk=newsitem_pk)
    news_form = NewsForm(data=data,
                         instance=news_item)
    if news_form.is_valid():
        news_form.save()
        return HttpResponseRedirect(reverse('news_list'))
    return render_to_response('news/news_edit.html',
                              {'news_form': news_form},
                              context_instance=RequestContext(request))