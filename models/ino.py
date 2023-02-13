from mongoengine import *
from mongoengine.queryset.visitor import Q
import datetime
import re
from dateutil.parser import *
from dateutil.tz import *
from dateutil.relativedelta import *
from logger import *

class Ino_news(Document):
    news_id = IntField()
    title = StringField(max_length=255)
    anons = StringField(max_length=255)
    date_create = DateTimeField()
    edition = StringField()
    page_name = StringField()
    meta = {"db_alias":"default"}    

    @classmethod
    def find_article(cls, urldate, name):
        date = parse(urldate)
        date1 = date + datetime.timedelta(days=1)
        date1 = parse(date1.strftime("%Y-%m-%d"))
        res = None
        try:
            res = cls.objects.get( Q(page_name=name) & Q(date_create__gte=date) & Q(date_create__lte=date1) )
        except Exception as ex:
            print('news not found ex={}'.format(ex))
            return
        return res

    @classmethod
    def find_article_by_url(cls, url):
        url = re.sub('pwa\/','',url)
        res = re.search(r'https:\/\/www\.inopressa\.ru\/article\/(\d\d\w\w\w\d\d\d\d)\/(\w+)\/([\w\d\_\-]+)\.html$', url)
        if res:
            news = cls.find_article(res.group(1),res.group(3))
            if news:
                return news
        return
        