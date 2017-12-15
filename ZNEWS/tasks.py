import logging

from datetime import timedelta

from NSproject import celery_app
from scrapy.crawler import CrawlerProcess
from scrapy_spiders.scrapy_spiders.spiders import qutes_spider
from celery.schedules import crontab

logger = logging.getLogger('spyder_task')


@celery_app.task
def add(x, y):
    logger.info('Task start')
    print(x + y)


@celery_app.task(time_limit=20)
def update():
    process = CrawlerProcess()
    logger.info('Create process')
    process.crawl(qutes_spider.QuotesSpider)
    logger.info('Start Crawl')
    process.start(stop_after_crawl=False)
    logger.info('update successful')
#
# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(60.0, update(), name='update')



