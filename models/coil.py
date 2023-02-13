from mongoengine import *
from mongoengine.queryset.visitor import Q
import datetime
import re
from dateutil.parser import *
from dateutil.tz import *
from dateutil.relativedelta import *


class Coil_news(Document):
    news_id = IntField()
    title = StringField(max_length=255)
    anons = StringField(max_length=255)
    date_create = DateTimeField()
    topic_id = IntField()
    page_name = StringField()
    meta = {"db_alias":"default"}    

    @classmethod
    def find_article(cls, topic, urldate, name):
        topics = {"israel":"1", "world":"2", "finance":"3", "mideast":"4", "sport":"5", "rest":"6", "press":"7", "election":"20", "realty":"21","auto":"22","health":"24","photo":"25"}
        date = parse(urldate)
        date1 = date + datetime.timedelta(days=1)
        date1 = parse(date1.strftime("%Y-%m-%d"))
        res = None
        try:
            res = cls.objects.get( Q(page_name=name) & Q(topic_id=topics[topic]) & Q(date_create__gte=date) & Q(date_create__lte=date1) )
            res.topic = topic
        except Exception as ex:
            print('news not found ex={}'.format(ex))
            return
        return res

    @classmethod
    def find_article_by_url(cls, url):
        res = re.search(r'https:\/\/www\.newsru\.co\.il\/(\w+)\/(\d\d\w\w\w\d\d\d\d)\/([\w\d\_\-]+)\.html$', url)
        if res:
            news = cls.find_article(res.group(1),res.group(2),res.group(3))
            if news:
                return news
        return
        