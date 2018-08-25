import logging
from datetime import date

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s  <%(funcName)s %(module)s.py:%(lineno)d>',
                    datefmt='%H:%M:%S',
                    filename='scrape_{}.log'.format(str(date.today())))
