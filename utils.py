import re
import sys
import datetime
from datetime import timedelta
import hashlib
from logger import *
from conf_rss import *

class UtilsMixin:
	@classmethod
	def topic_rus_date(cls):
		return cls.rus_date_genitive((datetime.datetime.now() + timedelta(seconds=10800)).strftime("%A, %d %B %Y г."))

	"""
	Starting working with image(s) for news method
	"""
	@classmethod
	def image(cls, n, request):
		phts = []
		ph_onlist_pos = list(filter(lambda x: x['on_list'] == 1, n.photos))[0]['position']
		l_ph = list(filter(lambda x: x['is_large'] == 1, n.photos))
		for ph in l_ph:
			if 'turbo' in request.path or ph['position'] == ph_onlist_pos:
				phts = cls.add_image(n, ph, phts)
		return phts

	"""
	Adding more images to turbo news
	"""
	@classmethod
	def add_image(cls, n, ph, phts):
		md5key = '{}{}'.format(n.news_id, ph['photo_id'])
		ph['url'] = cls.img_url(md5key, n.topic_id, n.date_create)
		phts.append({'url':ph['url'], 'alt':ph['alt_text'], 'source_name':ph['source_name']})
		return phts

	"""
	Constracting exact image url
	"""
	@classmethod
	def img_url(cls,  md5key, topic_id, news_date):
		topic_format = '{0:02d}'.format(topic_id)
		md5_name = hashlib.md5(md5key.encode()).hexdigest()
		year_news = str(news_date.year)
		month_news = '{0:02d}'.format(news_date.month)
		photo_url = '/'.join([IMAGES_URL, topic_format, year_news, month_news, md5_name[:1], md5_name]) + ".jpg"
		return photo_url

	"""
	Adding genitive case to monthes
	"""
	@classmethod
	def rus_date_genitive(cls, date):
		date = date.lower()
		date = re.sub(r'январь', 'января', date)
		date = re.sub(r'февраль', 'февраля', date)
		date = re.sub(r'март', 'марта', date)
		date = re.sub(r'апрель', 'апреля', date)
		date = re.sub(r'май', 'мая', date)
		date = re.sub(r'июнь', 'июня', date)
		date = re.sub(r'июль', 'июля', date)
		date = re.sub(r'август', 'августа', date)
		date = re.sub(r'сентябрь', 'сентября', date)
		date = re.sub(r'октябрь', 'октября', date)
		date = re.sub(r'ноябрь', 'ноября', date)
		date = re.sub(r'декабрь', 'декабря', date)
		return date

	"""
	Cutting main domain and https:// from urls to make them relative
	"""
	@classmethod
	def cut_domain(cls, url):
		url = re.sub(BASE_PATTERN2, BASE_URL, url)
		if url.startswith('/'):
		   url = BASE_URL + url
		return url   

	"""
	Bunch of regexps for cleaning text 
	"""
	@classmethod
	def edit_text(self, new_text):
		p_main_pattern = '(.{4}<p class="maintext">)'
		main_class = re.findall('((<p class="maintext">){2,})', new_text)
		all_main_class = [item[0] for item in main_class]
		for item in all_main_class:
			new_text = re.sub(item, '<p class="maintext">', new_text)
		new_text = re.sub(r'\{pic\s\w\}', '', new_text)
		return new_text

