from mongoengine import *
from mongoengine.queryset.visitor import Q
import datetime
from dateutil.parser import *
from dateutil.tz import *
from dateutil.relativedelta import *
import re
import sys
import os
import hashlib
from logger import *
from models.topics import Topics
sys.path.append('/opt/web/conf')
from conf_rss import *
def dbconnn(als):
	dbc = None
	try:
		dbc = connect(
			db=MONGO_DBNAME, 
			username=MONGO_USERNAME, 
			password=MONGO_PASSWORD,
			host=MONGO_HOST,
			port=MONGO_PORT, 
			uuidRepresentation='standard',
			authentication_source=MONGO_AUTH_SOURCE,
			alias=als,
		)
	except Exception as ex:
		print('cant connect to db {}'.format(ex))
	return dbc

d=dbconnn("default")



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
	photos = ListField()
	links = ListField()
	blog_url = StringField()

	topic = ''
	topic_id = 0


	def img_url(self, photo_id, news_id, news_date):
		topic_format = str('{0:02d}'.format(self.topic_id))
		md5_name = hashlib.md5((str(news_id) + str(photo_id)).encode()).hexdigest()
		year_news = str(news_date.year)
		month_news = str('{0:02d}'.format(news_date.month))
		photo_url = '/'.join([IMAGES_URL, topic_format, year_news, month_news, md5_name[:1], md5_name]) + ".jpg"
		return photo_url

	@classmethod
	def news_count(cls):
		res = cls.objects.count()
		return res		

	@classmethod
	def get_last_news(cls):
		return cls.objects().order_by('-date_create').limit(1)[0]
		
	@classmethod
	def news_count_date(cls):
		date = datetime.date.today()
		tmw = date + datetime.timedelta(days=1)
		try:
			res = cls.objects( Q(date_create__gte=date) & Q(date_create__lt=tmw) ).count()		
		except Exception as ex:
			res = 0
			logger.error('cant count news {} {} {}'.format(cls.topic, date, ex))
		return res	 

	@classmethod
	def topic_photos(cls, allnews_cnt=None):
		res = None
		if allnews_cnt is None:
			count = cls.news_count_date()
		else:
			count = allnews_cnt
		tmw = datetime.date.today() + datetime.timedelta(days=1)
		if count>19:
			limit = 200
			res = cls.objects( Q(date_create__gte=datetime.date.today()) & Q(date_create__lt=tmw) )
		else:
			if allnews_cnt is not None:
				limit = 4
			else:
				limit = 50
			res = cls.objects( Q(date_create__lt=tmw) ).order_by('-date_create').limit(limit)
		return res  

	@classmethod
	def turbo_news(cls, allnews_cnt=None):	 
		res = None   
		try:
			res = cls.objects( Q(date_create__lt=datetime.date.today()) ).order_by('-date_create').limit(114)
		except Exception as ex:
			logger.error(ex)
			return
		return res
	
	@classmethod
	def find_article(cls, urldate, name):
		date = parse(urldate)
		date1 = date + datetime.timedelta(days=1)
		date1 = parse(date1.strftime("%Y-%m-%d"))
		res = None
		try:
			res = cls.objects.get( Q(page_name=name) & Q(date_create__gte=date) & Q(date_create__lte=date1) )
		except Exception as ex:
			logger.error('news not found ex={}'.format(ex))
			return
		return res




d2 = Topics.objects(Q(is_active=1) & Q(eng_name__ne='promo')).all()
topics = list(map(lambda x: x['eng_name'], d2))
for new in topics:
	find_topic = next(filter(lambda x: x['eng_name'] == new, d2))
	top_id = find_topic['topic_id']
	topic_rus = find_topic['rus_name']
	cnt_title = find_topic['cnt_title']
	cnt_photo = find_topic['cnt_photo']
	position = find_topic['position']
	db_als='als' + str(find_topic['position'])
	db=dbconnn(db_als)
	setattr(sys.modules[__name__], new.capitalize() + "News",
			type(new.capitalize() + "News", (New, Document),
				{"__tablename__": new + '_news', "topic": new.lower(), "eng_name": new.lower(),  "topic_id": top_id, "topic_rus": topic_rus, "rus_name": topic_rus, "cnt_title": cnt_title, "cnt_photo": cnt_photo, "position":position,"meta":{"db_alias":db_als}}))
				
del d2				