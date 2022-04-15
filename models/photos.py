from mongoengine import *
from mongoengine.queryset.visitor import Q
import datetime
import re
import sys
import os
from models.topics import Topics
import hashlib


class Photos:
    photo_id = IntField()
    old_id = IntField()
    news_id = IntField()
    position = IntField()
    is_large = IntField()
    alt_text = StringField(max_length=255)
    source_name = StringField(max_length=255)
    source_url = StringField(max_length=255)
    date_create = DateTimeField()
    on_list = IntField()
    hide_copyright = IntField()

    topic = ''
    topic_id = 0

    def img_url(self, photo_id, news_id, news_date):
        # topic_img = TopicsModel.find_topic_id(self.topic)[0]
        topic_format = str('{0:02d}'.format(self.topic_id))
        md5_name = hashlib.md5((str(news_id) + str(photo_id)).encode()).hexdigest()
        year_news = str(news_date.year)
        month_news = str('{0:02d}'.format(news_date.month))
        photo_url = '/'.join(["https://image.newsru.com/v2", topic_format, year_news, month_news, md5_name[:1], md5_name]) + ".jpg"
        return photo_url

    @classmethod
    def find_by_news_id(cls, news):
        res = cls.objects(news_id=news).all()
        return res

    @classmethod
    def find_by_news_id_on_list(cls, news_id):
        res = cls.objects(news_id=news_id,on_list=1).limit(1)
        return res

    @classmethod
    def find_lasts_img(cls, count):
        return cls.objects.order_by('+date_create').limit(count)


d2 = Topics.objects(is_main_menu=1).all()
topics = list(map(lambda x: x['eng_name'], d2))

for new in topics:
    find_topic = next(filter(lambda x: x['eng_name'] == new, d2))
    top_id = find_topic['topic_id']
    setattr(sys.modules[__name__], new.capitalize() + "NewsPhotos",
            type(new.capitalize() + "NewsPhotos", (Photos, Document),
                 {"__tablename__": new + '_news_photos', "topic": new.lower(), "topic_id": top_id}))



