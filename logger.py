import logging
from logging.handlers import RotatingFileHandler
#from config.config import get_config_setting


#handler = RotatingFileHandler(settings.LOGGER, maxBytes=1000000, backupCount=1, encoding='utf-8')
handler = RotatingFileHandler('/var/log/rss/rss-error.log', maxBytes=1000000, backupCount=1, encoding='utf-8')
formatter = logging.Formatter(" [%(asctime)s - %(name)s - %(filename)s:%(lineno)s - %(funcName)s()] %(message)s")

handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

"""
when create a container, need to mount log dir
>>> -v path/to/log/on/hostmachine:/var/log/raa

USAGE:
for all moduls
>>> from libs.logger import *

to print a log to a file, you must write
>>> logger.info('mesage', 'topic')
"""

