from django.shortcuts import render
from django.views.generic import ListView
from .models import News, Laws
import feedparser
import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


# @method_decorator(cache_page(60*60), name="dispatch")
# @method_decorator(vary_on_cookie, name="dispatch")
class NewsListView(ListView):
    """Listing of news"""
    template_name = 'news/news-list.html'
    paginate_by = 10

    
    def get_queryset(self):

        news = []

        for src in News.objects.all():
            url = src.rss_url
            fdate = src.date_format
            author_title = src.publisher
            tags = src.tags
            query_srch = tags.split()

            try:
                posts = feedparser.parse(url)
            except Exception as err:
                print(err)
                continue

            for post in posts['entries']:
                if query_srch:
                    for tag in query_srch:
                        if tag:
                            if tag in post.get('title') or tag in post.get('description'):
                                title = post.get('title')
                                link = post.get('link')
                                content = post.get('description')
                                if post.get('enclosures'):
                                    image = post.get('enclosures')[0]['href']
                                else:
                                    image = None
                                published = datetime.datetime.strptime(
                                    post.get('published'), fdate).strftime('%d.%m.%Y %H:%M')
                                news.append(
                                    [published, title, content, link, author_title, image, ])
                                break
                            else:
                                continue
                        else:
                            continue
                else:
                    title = post.get('title')
                    link = post.get('link')
                    content = post.get('description')
                    if post.get('enclosures'):
                        image = post.get('enclosures')[0]['href']
                    else:
                        image = None
                    published = datetime.datetime.strptime(
                        post.get('published'), fdate).strftime('%d.%m.%Y %H:%M')
                    news.append([published, title, content,
                                 link, author_title, image, ])

        return sorted(news, key=lambda new: datetime.datetime.strptime(new[0], '%d.%m.%Y %H:%M'), reverse=True)


# @method_decorator(cache_page(60*60), name="dispatch")
# @method_decorator(vary_on_cookie, name="dispatch")
class LawsListView(ListView):
    """Listing of laws"""
    template_name = 'news/laws-list.html'
    paginate_by = 10

    def get_queryset(self):

        laws = []

        for src in Laws.objects.all():
            url = src.rss_url
            fdate = src.date_format
            author_title = src.publisher
            tags = src.tags
            query_srch = tags.split()

            try:
                posts = feedparser.parse(url)
            except Exception as err:
                print(err)
                continue
                
            for post in posts['entries']:
                if query_srch:
                    for tag in query_srch:
                        if tag:
                            if tag in post.get('title') or tag in post.get('description'):
                                title = post.get('title')
                                link = post.get('link')
                                content = post.get('description')
                                if post.get('enclosures'):
                                    image = post.get('enclosures')[0]['href']
                                else:
                                    image = None
                                published = datetime.datetime.strptime(
                                    post.get('published'), fdate).strftime('%d.%m.%Y %H:%M')
                                laws.append(
                                    [published, title, content, link, author_title, image, ])
                                break
                            else:
                                continue
                        else:
                            continue
                else:
                    title = post.get('title')
                    link = post.get('link')
                    content = post.get('description')
                    if post.get('enclosures'):
                        image = post.get('enclosures')[0]['href']
                    else:
                        image = None
                    published = datetime.datetime.strptime(
                        post.get('published'), fdate).strftime('%d.%m.%Y %H:%M')
                    laws.append([published, title, content,
                                 link, author_title, image, ])
            
        return sorted(laws, key=lambda new: datetime.datetime.strptime(new[0], '%d.%m.%Y %H:%M'), reverse=True)
    