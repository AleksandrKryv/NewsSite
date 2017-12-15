import sys
import os
import django
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_djangoitem import DjangoItem



sys.path.append('/home/alex/projects/NSproject')
os.environ['DJANGO_SETTINGS_MODULE'] = 'NSproject.settings'
django.setup()
from ZNEWS.models import *
from django.db.models import F

class NewsItem(DjangoItem):
    django_model = NewsPost


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    post_img = {}
    categories = {
        "https://news.tut.by/economics": "Economics and Politics",
        "https://news.tut.by/world/": "World",
        "https://news.tut.by/society/": "Society",
        "https://news.tut.by/auto/": "Auto",
        "https://auto.tut.by/news/autonews/": "Auto",
        "https://auto.tut.by/news/exclusive/": "Auto",
        "https://auto.tut.by/news/road/": "Auto",
        "https://auto.tut.by/news/autobusiness/": "Auto",
        "https://news.tut.by/accidents/": "Accidents",
        "https://auto.tut.by/news/accidents/": "Accidents",
        "https://42.tut.by/": "Tech",
        "https://news.tut.by/it/": "Tech",
        "https://news.tut.by/sport/": "Sport",
        "https://sport.tut.by/": "Sport",
        "https://sport.tut.by/news/aboutsport": "Sport",
        "https://news.tut.by/realty": "Realty",
        "https://realty.tut.by/": "Realty",
        "https://news.tut.by/go/": "Health",
    }

    banned_categories = [
        "help.blog.tut.by",
    ]

    def start_requests(self):
        urls = [
            "https://news.tut.by/economics/",
            "https://news.tut.by/world/",
            "https://news.tut.by/society/",
            "https://news.tut.by/auto/",
            "https://news.tut.by/accidents/",
            "https://news.tut.by/it/",
            "https://news.tut.by/sport/",
            "https://news.tut.by/realty/",
            "https://news.tut.by/go/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        newspost = NewsItem()
        for post in response.css("div.col-w div.news-entry"):
            newspost['post_photo'] = post.css("a img::attr(src)").extract_first()
            post_url = post.css("a::attr(href)").extract_first()
            post_photo = post.css("a img::attr(src)").extract_first()
            self.post_img.update({post_url: post_photo})
            for banned_category in self.banned_categories:
                if banned_category not in post_url:
                    if not NewsPost.objects.filter(post_source=post_url):

                        yield response.follow(post_url, callback=self.parse_post)

    def parse_post(self, response):
        newspost = NewsItem()
        newspost['post_source'] = response.url
        for category in self.categories:
            if category in response.url:
                category, created = Category.objects.get_or_create(category_name=self.categories[category])
                newspost['post_category'] = category
        for url in self.post_img:
            if url == response.url:
                newspost['post_photo'] = self.post_img[url]
        newspost['post_header'] = response.css("div.b-article div.m_header h1::text").extract_first()
        for text in response.css("div.js-mediator-article"):
            photo = text.css("figure.image-captioned img::attr(src)").extract()
            post_content = "<br></br>".join(text.css("p ::text").extract())
            print(post_content)
            newspost['post_content'] = post_content
            if photo is not None:
                for photo in photo:
                    newspost['post_content'] += u'<img src={} style="text-align:center;">'.format(photo)
        if not NewsPost.objects.filter(post_source=newspost['post_source']):
            newspost.save()

# def prcstart():
#     process = CrawlerProcess()
#     process.crawl(QuotesSpider)
#     process.start(stop_after_crawl=False)
#     process.stop()
#
# prcstart()