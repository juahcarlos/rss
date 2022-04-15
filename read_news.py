from datetime import *
from itertools import chain
from multiprocessing.dummy import Pool
import time
import hashlib
import re
import inspect
from dateutil.parser import *
from dateutil.tz import *
from dateutil.relativedelta import *
from logger import *
from settings import *
from utils import *
import models.news
import models.photos
import models.topics
from models.notes import *
from models.topics import *
from models.hotnews import *
from models.spiegels import *

"""
Make regular classes from `partitions` `fabrique`
"""
class ModelsNews:
	def _models(self):
		res = [j for i, j in inspect.getmembers(models.news, inspect.isclass) if i.endswith("News") and j.position > 1 and j.cnt_title > 0]
		return res

	def my_model(self, topic):
		res = [j for j in self._models() if j.topic == topic][0]
		return res	

"""
Preparing queries before call models for topics type feeds
"""
class ReadNews(ModelsNews):
	def _turbo_news_q(self, topic, allnews_cnt=None):
		return self.my_model(topic).turbo_news(allnews_cnt)

	def _regular_news_q(self, topic, allnews_cnt=None):
		return self.my_model(topic).topic_photos(allnews_cnt)

	def _news_q(self, topic, allnews_cnt=None):
		if self.turbo():
			return self._turbo_news_q(topic, allnews_cnt)
		else:
			return self._regular_news_q(topic, allnews_cnt)

"""
Formating data for topics views
"""
class FormatAll:
	def format_news(self, nws):
		raise NotImplementedError("method format_news should be implemented")

"""
Formating data for topics views
"""		
class FormatTopic(FormatAll):
	def format_news(self, nws):
		news = []
		for n in nws:
			md5key = '{}{}'.format(n.news_id, n.photo_id)
			n.image = self.img_url(md5key, n.topic_id, n.date_create)
			n.text = self.edit_text(n.text)
			n.host = BASE_URL
			n.author = self._author(n.note_id, n.eng_name)
			n.title = self.clear_title(n.title)
			n.topic_rus_name = n.rus_name
			news.append(n)
		return news

	def clear_title(self, title):
		if self.turbo():
			title = re.sub("&39;", "'", title)
		else:
			title = re.sub('\&', '&amp;', title)
		return title

	def _author(self, note_id, topic):
		if topic == 'blog':
			note = Notes().note_by_id(note_id)
			return note.rus_name

"""
Formating data for google views
"""		
class FormatGoogle(FormatAll):
	def format_news(self, nws, **kwargs):
		news = []
		for ns in nws:
			ns.phts = self.image(ns, self.request)
			ns.text = self.edit_text(ns.text)
			ns.topic = ns.rus_name
			ns = self.google_format_news(ns, **kwargs)
			news.append(ns)
		return news
		
	def google_format_news(self, ns, **kwargs):
		if kwargs.get('google') == 1:
			ns.text = self.clear_tags_for_google(ns.text)
			if len(ns.phts) > 0:
				ns.guid = hashlib.md5((str(ns.topic_id) + str(ns.news_id)).encode()).hexdigest()
			if not hasattr(ns, 'host'):
				ns.host = BASE_URL		
		return ns
			
	def clear_tags_for_google(self, text):
		res = re.sub(r'<blockquote.+?\/blockquote>', '', text)
		res = re.sub(r'<script.+?\/script>', '', res)
		return res

"""
Receiving data for topics views
"""
class TopicRSS(UtilsMixin, FormatAll, ReadNews):
	def allnews(self):
		allnews_cnt = self.allnews_count_date()
		topics = Topics.topics_main_menu()
		if self.turbo:
			news = self.loop_news_by_topics_multi(topics, allnews_cnt)
		else:
			news = self.loop_news_by_topics(topics, allnews_cnt)
		news.sort(key=lambda k: k.date_create, reverse=True)
		news = self.format_news(news)
		return news[0:self.limit()]

	def loop_news_by_topics_multi(self, topics, allnews_cnt):
		news = []
		pool = Pool(5)
		for topic in topics:
			nst = pool.apply_async(self._turbo_news_q, (topic.eng_name, allnews_cnt)).get()
			news.extend(nst)
		return news

	def loop_news_by_topics(self, topics, allnews_cnt):
		news = []
		for topic in topics:
			nst = self._regular_news_q(topic.eng_name, allnews_cnt)
			news.extend(nst)
		return news

	def get_topic_news_ename(self, eng_name):
		res = self.format_news(self._regular_news_q(eng_name))
		return res

	def limit(self):
		turbo_length = {True:1000, False:50}
		return turbo_length['turbo' in self.request.path]

	def turbo(self):
		return 'turbo' in self.request.path

	def allnews_count_date(self):
		count = 0
		for model in self._models():
			count += model.news_count_date()
		return count

	def topic_rus_name(self, eng_name=""):
		topic = Topics.get_topic_by_eng_name(eng_name)
		return topic.rus_name
	
"""
Preparing queries before call models for spiegels type feeds
"""
class ReadSpgHot(UtilsMixin, ModelsNews):
	def spgnews(self):
		res = list(chain(Spiegels.findall(), Hotnews.findall().all()))
		res = list(map(self.get_one_news, res))
		return res
		
	def get_one_news(self, n):
		nws = None
		if re.match(MAIN_PATTERN, n.url) or n.url.startswith('/'):
			nws = self.get_one_news_for_spiegel_by_url(n.url)
			n.eng_name = nws.eng_name
			n.topic = nws.topic_rus
			n.topic_rus = nws.topic_rus
			n.host = BASE_URL
			if hasattr(n, 'text') and n.position == 1:
				n.anons = n.text
			else:
				n.anons = nws.anons
		if hasattr(nws, 'date_create'):
			n.date_create = nws.date_create
		n.page_name = nws.page_name
		return n		

	def get_one_news_for_spiegel_by_url(self, url):
		if re.match(MAIN_PATTERN, url):
			res = re.search(r'\/(\w+)\/(\d\d\w\w\w\d\d\d\d)\/([\w\d\_\-]+).html', url)
			if res:
				try:
					news = self.my_model(res.group(1)).find_article(res.group(2), res.group(3))
					return news
				except Exception as ex:
					logger.error('get_one_news_for_spiegel news not found utl={} ex={}'.format(url, ex))
		return

