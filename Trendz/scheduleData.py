from apscheduler.schedulers.background import BackgroundScheduler
from .scrap import scraplaptop, scrapmobile
from .twitterApi import mobiledaily_trend, mobileweekly_trend, laptopweekly_trend, Laptopdaily_trend


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scraplaptop, 'cron',
                      day_of_week='mon', hour=16, minute=44)
    scheduler.add_job(scrapmobile, 'cron',
                      day_of_week='mon', hour=19, minute=8)
    scheduler.add_job(mobiledaily_trend, 'cron', hour=00, minute=43)
    scheduler.add_job(mobileweekly_trend, 'cron',  hour=15, minute=40)
    scheduler.add_job(Laptopdaily_trend, 'cron', hour=17, minute=18)
    scheduler.add_job(laptopweekly_trend, 'cron',  hour=17, minute=20)
    scheduler.start()
