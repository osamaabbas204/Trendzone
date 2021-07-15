from apscheduler.schedulers.background import BackgroundScheduler
from .scrap import scraplaptop, scrapmobile, popularMobile, latestMobile, popularLaptop
from .twitterApi import mobiledaily_trend, mobileweekly_trend, laptopweekly_trend, Laptopdaily_trend
from .views import email


def start():

    scheduler = BackgroundScheduler()
    # Schedulers for scraping functionality
    scheduler.add_job(scraplaptop, 'cron',
                      day_of_week='tue', hour=10, minute=17)
    scheduler.add_job(scrapmobile, 'cron',
                      day_of_week='tue', hour=10, minute=19)
    scheduler.add_job(latestMobile, 'cron',
                      day_of_week='tue', hour=10, minute=22)
    scheduler.add_job(popularMobile, 'cron',
                      day_of_week='tue', hour=10, minute=25)
    scheduler.add_job(popularLaptop, 'cron',
                      day_of_week='tue', hour=10, minute=28)
    # Schedulers for trendz
    scheduler.add_job(mobiledaily_trend, 'cron', hour=10, minute=30)
    scheduler.add_job(mobileweekly_trend, 'cron',
                      day_of_week='tue',  hour=10, minute=32)
    scheduler.add_job(Laptopdaily_trend, 'cron', hour=10, minute=34)
    scheduler.add_job(laptopweekly_trend, 'cron',
                      day_of_week='tue',  hour=10, minute=36)
    # Schedulers for Email
    scheduler.add_job(email, 'cron', day_of_week='mon', hour=20, minute=15)
    # All Schedulers Start
    scheduler.start()
