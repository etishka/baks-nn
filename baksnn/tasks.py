from celery import Celery
from crawlers import crawlers

celery = Celery('tasks',
#                backend='amqp',
#                broker='amqp://guest@localhost//'
                backend='redis',
                broker='redis://localhost'
                )

@celery.task
def run_crawlers():
    res = []
    for bank in crawlers:
        crawler = bank()
        res.append((crawler.get_name(), crawler.get_usd_buy(), crawler.get_usd_sell(),))
    
