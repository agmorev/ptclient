# Create your tasks here
from ptclient.celery import app
from news.models import News
import feedparser
# from celery import shared_task


@app.task
def news_parser():
    news = []

    for src in News.objects.all():
            publisher = src.publisher
            url = src.rss_url
            fdate = src.date_format
            posts = feedparser.parse(url)
            author_title = src.publisher
            tags = src.tags

            query_srch = tags.split()

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

# @shared_task
# def add(x, y):
#     return x + y

# @shared_task
# def mul(x, y):
#     return x * y

# @shared_task
# def xsum(numbers):
#     return sum(numbers)
