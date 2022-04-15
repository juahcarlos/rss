import re
import time
import datetime
import memcache
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import generic
from django.views import View
from dateutil.parser import *
from dateutil.tz import tzoffset, tzlocal
from read_news import *
from utils import *
from settings import *
from logger import *


class Cache:
	def __init__(self):
		self.cache = []
		for a in CACHE["host"]:
			mc = memcache.Client([a])
			if mc is not None:
				self.cache.append(mc) 

	def set(self, request, value):
		key = '{}:{}'.format(CACHE["namespace"],request.path)
		if len(key)<250:
			for c in self.cache:
				c.set(key, value, CACHE["mc_time"])

	def get(self, key):
		return self.cache[0].get(key)

class Err404(View):
	def get(self, request):
		res = render(request, 'error404.html', {})
		response = HttpResponse(res, content_type='text/html; charset=utf-8')
		response.status_code = 404
		return response

class Err500(View):
	def get(self, request):
		res = render(request, 'error500.html', {})
		response = HttpResponse(res, content_type='text/html; charset=utf-8')
		response.status_code = 500
		return response

class Robots(View):
	def get(self, request):
		res = render(request, 'robots.html', {})
		response = HttpResponse(res, content_type='text/plain; charset=utf-8')
		return response

class Rend():
	def result(self, **kwargs):
		params = dict(**kwargs)
		params['now'] = datetime.datetime.now() + timedelta(seconds=10800)
		template = params.get('template', 'topic') + '.html'
		response = render(self.request, template, params)
		response['Content-type'] = 'application/rss+xml'
		Cache().set(self.request,response.content)
		return response

class AllnewsGet(View, TopicRSS, FormatTopic, Rend):
	def get(self, request):
		return self.result(
			news=self.allnews(),
			topic_rus_name="Все новости",
			eng_name='allnews'
		)

class TopicGet(View, TopicRSS, FormatTopic, Rend):
	def get(self, request, eng_name):
		topic_rus_name = self.topic_rus_name(eng_name)
		return self.result(
			news=self.get_topic_news_ename(eng_name),
			topic_rus_name=topic_rus_name,
			eng_name=eng_name
		)

class Big(View, ReadSpgHot, Rend):
	def get(self, request):
		news = self.spgnews()
		return self.result(
			news=news,
			topic_rus_name='Главные новости',
			topic_rus_date=self.topic_rus_date(),
			eng_name='allnews'
		)

class Main(View, TopicRSS, FormatTopic, Rend):
	def get(self, request):
		base = self.allnews()
		news = list(filter(lambda x: x.show_type!=0, base))[0:50]
		news.sort(key=lambda k: k['date_create'], reverse=True)
		return self.result(
			main = 1,
			news=news,
			topic_rus_name='Важные новости'
		)

class GoogleAllRSS(TopicRSS, FormatGoogle, Rend):
	def get_n(self, request, **kwargs):
		news = self.allnews()
		return self.result(
			news=news,
			topic_rus_name="Все новости",
			topic_rus_date=self.topic_rus_date(),
			base_url=BASE_URL,
			yandex=kwargs.get('yandex'),
			zen=kwargs.get('zen'),
			interfax=kwargs.get('interfax'),
			mail=kwargs.get('mail'),
			rambler=kwargs.get('rambler'),
			google=kwargs.get('google'),
		)

class GoogleRSS(TopicRSS, FormatGoogle, Rend):
	def get_n(self, request, eng_name=None, **kwargs):
		news = self.get_topic_news_ename(eng_name)
		return self.result(
			news=news,
			topic_rus_name=self.topic_rus_name(eng_name),
			topic_rus_date=self.topic_rus_date(),
			eng_name=eng_name,
			base_url=BASE_URL,
		)

class FBYandex(GoogleRSS, FormatGoogle, Rend):
	def news(self, request, name):
		news = self.allnews()
		return self.result(
			template=name,
			news=news,
			topic_rus_name="Все новости",
			topic_rus_date=self.topic_rus_date(),
			base_url=BASE_URL
		)

class Google(View, GoogleRSS):
	def get(self, request, eng_name):
		return self.get_n(request, eng_name, google=1)

class GoogleAll(View, GoogleAllRSS):
	def get(self, request):
		logger.error('GoogleAllGoogleAllGoogleAllGoogleAllGoogleAllGoogleAllGoogleAll')
		return self.get_n(request, google=1)

class Mail(View, GoogleAllRSS):
	def get(self, request):
		return self.get_n(request, mail=1)

class Rambler(View, GoogleAllRSS):
	def get(self, request):
		return self.get_n(request, rambler=1)

class Interfax(View, GoogleAllRSS):
	def get(self, request):
		return self.get_n(request, interfax=1)
class Yandex(View, GoogleAllRSS):
	def get(self, request):
		return self.get_n(request, yandex=1)

class YandexZen(View, FBYandex):
	def get(self, request):
		return self.news(request, 'zen')

class YandexTurbo(View, FBYandex):
	def get(self, request):
		logger.error('YandexTurbo')
		return self.news(request, 'turbo')

class Facebook(View, FBYandex):
	def get(self, request):
		return self.news(request, 'facebook')