import schedule
import time

import modules.product as pr
Product = pr.Product()
def checkNot():
    schedule.every().day.at("08:59").do(Product.dayPush)
    schedule.every().day.at("20:59").do(Product.nightPush)

    while True:
        schedule.run_pending()
        time.sleep(10)