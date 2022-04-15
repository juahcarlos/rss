from mongoengine import *
import datetime
import re
from dateutil.parser import *
from dateutil.tz import *
from dateutil.relativedelta import *

class MedNews(Document):
    news_id = IntField()
    date_create = DateTimeField()
    title = StringField(max_length=255)
    anons = StringField(max_length=255)
    page_name = StringField(max_length=255)
    image  = IntField()
    
    #meta = {"db_alias":"default"}

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
        res = re.search(r'http:\/\/www\.meddaily\.ru\/article\/(\d\d\w\w\w\d\d\d\d)\/([\w\d\_\-]+)$', url)
        if res:
            news = cls.find_article(res.group(1),res.group(2))
            if news:
                return news
        return
    
    