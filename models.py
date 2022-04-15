from mongoengine import *
from mongoengine.queryset.visitor import Q
import datetime
import re
import sys
import os
from django.db import models

try:
    connect(
        db='newsru_test_db', 
        username='newsru_rd', 
        password='Fon8Gu-Tere', 
        host='localhost', 
        port=27017, 
        authentication_source='admin'
    )
except Exception as ex:
    print('cant connect to db {}'.format(ex))

class Topics(Document):
    topic_id = IntField()
    rus_name = StringField(max_length=255)
    date_create = StringField(max_length=255)
    eng_name = StringField(max_length=255)
    cnt_title = IntField()
    position = IntField()
    cnt_photo = IntField()
    is_active = IntField()
    is_closed = IntField()
    is_main_menu = IntField()
    cnt_lastnews = IntField()
    #meta = {"db_alias":"default"}

    @classmethod
    def topics_main_menu(cls):
        res = cls.objects(is_main_menu=1)
        #print('res={}'.format(res))
        return res

    @classmethod
    def get_topic_by_eng_name(cls, eng_name):
        print("ENG_NAME={}".format(eng_name))
        res = cls.objects(eng_name=eng_name).first()
        print('res={}'.format(res))
        return res


class New:
    news_id = IntField()
    old_id = IntField()
    show_type = IntField()
    is_advert = IntField()
    is_special = IntField()
    date_create = DateTimeField()
    date_modify = DateTimeField()
    page_name = StringField(max_length=255)
    title = StringField(max_length=255)
    anons = StringField(max_length=255)
    text = StringField(max_length=255)
    note_id = IntField()
    is_hidden = IntField()
    editor_id = IntField()
    was_spiegel = IntField()
    is_correct = IntField()
    gnews_tags = StringField(max_length=255)
    photo_id = IntField()

#    meta = {
#        'indexes': [
#            {'name':'nid', 'fields':['news_id']},
#        ]}

    topic = ''
    topic_id = 0

    @classmethod
    def news_count(cls):
        res = cls.objects.count()
        #print('res={}'.format(res))
        return res 

    @classmethod
    def news_count_date(cls, date):
        res = cls.objects(date_create__date=date.date()).count()
        print('news_count_date res={}'.format(res))
        return res            

    @classmethod
    def index_photos(cls, cnt_photo):
        print(cnt_photo*2)
        res = cls.objects(show_type=1).limit(cnt_photo*2)
        print('res={}'.format(len(res)))
        return res        

    @classmethod
    def topic_photos(cls, date):
        res = None
        if cls.news_count_date(date)>19:
            res = cls.objects(date_create__date=date.date())
        else:
            date2weeks = date + relativedelta(days=-1)
            res = cls.objects( Q(date_create__date_gte=date2weeks.date()) & Q(date_create__date_lte=date.date()) ) 
        print('res={}'.format(len(res)))
        return res  

    @classmethod
    def index_titles(cls, cnt_title):
        res = cls.objects.limit(cnt_title)
        #print('res={}'.format(res))
        return res        


d2 = Topics.objects(is_main_menu=1).all()
topics = list(map(lambda x: x['eng_name'], d2))

for new in topics:
    find_topic = next(filter(lambda x: x['eng_name'] == new, d2))
    top_id = find_topic['topic_id']
    topic_rus = find_topic['rus_name']
    cnt_title = find_topic['cnt_title']
    cnt_photo = find_topic['cnt_photo']
    position = find_topic['position']

    setattr(sys.modules[__name__], new.capitalize() + "News",
            type(new.capitalize() + "News", (New, Document),
                 {"__tablename__": new + '_news', "topic": new.lower(), "eng_name": new.lower(),  "topic_id": top_id, "topic_rus": topic_rus, "cnt_title": cnt_title, "cnt_photo": cnt_photo, "position":position}))


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
    meta = {
        'indexes': [
#            {'name':'nid', 'fields':['news_id']},
            {'name':'nid_list', 'fields':['news_id','on_list']}
        ]}

    topic = ''
    topic_id = 0

    # @property
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
        #print('find_by_news_id={} {}'.format(news,res))
        return res

    @classmethod
    def find_by_news_id_on_list(cls, news_id):
        res = cls.objects(news_id=news_id,on_list=1).limit(1)
        #print('find_by_news_id_on_list={} {}'.format(news_id,res))
        return res

    @classmethod
    def find_lasts_img(cls, count):
        return cls.objects.order_by('+date_create').limit(count)


d2 = Topics.objects(is_main_menu=1).all()
topics = list(map(lambda x: x['eng_name'], d2))

# Фабрика классов на основе мета-класса type, автоматически формирует
# классы для работы с таблицами разделов новостей, которые есть в главном меню
for new in topics:
    find_topic = next(filter(lambda x: x['eng_name'] == new, d2))
    
    top_id = find_topic['topic_id']

    setattr(sys.modules[__name__], new.capitalize() + "NewsPhotos",
            type(new.capitalize() + "NewsPhotos", (Photos, Document),
                 {"__tablename__": new + '_news_photos', "topic": new.lower(), "topic_id": top_id}))



