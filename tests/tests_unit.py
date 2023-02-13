import pytest
import os
import sys
sys.path.append('/opt/web/conf')
import conf_rss
import requests
from django.test import RequestFactory
from views import *
from read_news import *
import models.topics


def test_404():
	view = Err404.as_view()
	request = RequestFactory().get('22-') 
	response = view(request)
	assert response.status_code == 404		

def test_500():
	view = Err500.as_view()
	request = RequestFactory().get('/5rxr6ud') 
	response = view(request)
	assert response.status_code == 500	

def test_robots_txt():
	view = Robots.as_view()
	request = RequestFactory().get('robots.html') 
	response = view(request)
	assert response.status_code == 200
	assert response['content-type'] == "text/plain; charset=utf-8"
	
'''	
module test for view AllnewsGet
creating instanse class and getting main data - news, checking if len>0, id of 1st elemtnt is int, testing if  result is str, len>0 and news.title in result
'''
@pytest.fixture(scope="module")
def Allnews():
	self = AllnewsGet()
	self.request = RequestFactory().get('all') 
	return self
	
def Allnws():
	self = AllnewsGet()
	self.request = RequestFactory().get('all') 
	return self	

@pytest.fixture(scope="module")
def GoogleAllnews():
	self = GoogleAllRSS()
	self.request = RequestFactory().get('google/all') 
	return self
		

class TestNewsResult:	
	def test_allnews_result_is_str(self, Allnews):	
		assert isinstance((Allnews.result().content.decode('utf-8')),str), f"\t test_allnews_result_is_str FAILED"

	def test_allnews_result_len_lt_0(self, Allnews):
		assert len(Allnews.result().content.decode('utf-8'))>0, f"\t test_allnews_result_len_lt_0 FAILED"	
	
"""
base class for checking main content list methods in view.AllnewsGet and read_news.TopicRSS classes inherited by 2 classes implementing fixture and usin all tests in  this parent 
"""	
class Newslist:	
	@pytest.fixture(scope="class")
	def newsfx():
		pass
	
	def test_news_ln_eq_50(self,newsfx):
		assert len(newsfx.allnews())==50, f"\t test_news_ln_eq_36 FAILED"		
	
	def test_news_id_is_int(self,newsfx):
		assert isinstance((newsfx.allnews()[0].news_id),int), f"\t test_allnews_id_is_int FAILED"

	def test_allnews_first_id(self,newsfx):
		assert newsfx.allnews()[0].news_id>0, f"\t test_allnews_len_lt_0 FAILED"

	def test_allnews_len_lt_0(self,newsfx):
		assert len(newsfx.allnews())>0, f"\t test_allnews_len_lt_0 FAILED"

	def test_allnews_result_title_is_in(self,newsfx):
		r = requests.get(f'http://{MONGO_HOST}:8021/all_news/')
		m=re.search(newsfx.allnews()[0].title, r.text, re.MULTILINE)
		assert m is not None, f"\t test_allnews_result_title_is_in"

"""
testing parent classes preparing data for views
"""
class TestAllnews(FormatTopic, Newslist):
	@pytest.fixture(scope="class")
	def newsfx(self, Allnews): 
		return Allnews
		
"""
TopicRSS::allnews
"""	
class TestAllnewsGoogle(FormatTopic, Newslist):
	@pytest.fixture(scope="class")
	def newsfx(self, GoogleAllnews): 
		return GoogleAllnews

"""
TopicRSS::format_news
"""
class TestTopicRSS(FormatTopic, TopicRSS, UtilsMixin):
	@pytest.fixture(scope="class")
	def newsfx(self, Allnews): 
		return Allnews

	def news(self,newsfx):	
		return self.format_news(newsfx.allnews())

	@pytest.fixture
	def format_allnews(self,newsfx):
		return self.news(newsfx)

	@pytest.fixture
	def n(self,newsfx):
		return self.news(newsfx)[0]
		
	@property
	def request(self):
		return Allnws().request		
	
	def test_allnew_is_not_none(self,newsfx):
		assert newsfx.allnews() is not None, f"\t test_allnews_is_not_none FAILED"	
			
	def test_format_news_is_not_none(self, format_allnews):
		assert format_allnews is not None, f"\t test_allnews_is_not_none FAILED"		
		
	def test_format_news_len_news(self, n):
		assert len(n)>0, f"\t test_allnews_is_not_none FAILED"
	
	def test_format_news_eq_len_news_and_fixt(self,newsfx):
		assert len(self.news(newsfx))==len(newsfx.allnews()), f"\t test_format_news_eq_len_news_and_fixt FAILED"
		
	def test_format_news_len_phts_gt_0(self, n):
		assert len(n.image)>0, f"\t test_format_news_len_phts_gt_0 FAILED"	

	def test_format_news_phts_url(self, n):
		assert 'https://image.' in n.image and '.jpg' in n.image and re.search(r'/v2/\d{2}/\d{4}/\d{2}/\w/[\d\w]{32}',n.image), f"\t test_format_news_phts_url FAILED"		
			
	def test_format_news_len_text(self, n):		
		assert len(n.text)>20, f"\t test_format_news_len_text FAILED"
	
	def test_format_news_text(self, n):		
		assert re.match(r'[\w]+', n.text), f"\t test_format_news_text FAILED"
		
	def test_format_news_text(self, n):		
		assert re.match(r'[\w]+', n.text), f"\t test_format_news_text FAILED"		

	"""
	TopicRSS::other
	"""		
	def test_clear_title(self,newsfx):	
		assert newsfx.clear_title("ee xx&uu")=="ee xx&amp;uu", f"\t test_clear_title FAILED"	
		
	def test_topic_rus_name(self,newsfx):
		assert newsfx.topic_rus_name('sport') == 'Спорт', f"\t test_topic_rus_name FAILED"		
		
"""
TopicRSS::format_news
"""
class TestGoogleRSS(FormatGoogle, TopicRSS, UtilsMixin):
	@pytest.fixture(scope="class")
	def newsfx(self, Allnews): 
		return Allnews

	def news(self,newsfx):	
		return self.format_news(newsfx.allnews())

	@pytest.fixture
	def format_allnews(self,newsfx):
		return self.news(newsfx)

	@pytest.fixture
	def n(self,newsfx):
		return self.news(newsfx)[0]

	@property
	def request(self):
		return Allnws().request
		
	def test_format_news_len_phts_gt_0(self, n):
		assert len(n.phts)>0, f"\t test_format_news_len_phts_gt_0 FAILED"
		
	def test_format_news_phts_url(self, n):
		assert 'https://image.' in n.phts[0]['url'] and '.jpg' in n.phts[0]['url'] and re.search(r'/v2/\d{2}/\d{4}/\d{2}/\w/[\d\w]{32}',n.phts[0]['url']), f"\t test_format_news_phts_url FAILED"
		
	def test_clear_tags_for_google(self):
		assert self.clear_tags_for_google('<blockquote xxx>lala</blockquote>')=='', f"\t test_clear_tags_for_google FAILED"		
		
"""
Turbo
"""
class TestReadSpgHot(ReadSpgHot):
	@pytest.fixture(scope="class")
	def ReadSH(self):
		res = ReadSpgHot()
		return res
	
	def test_spg(self,ReadSH):
		sp = ReadSH.spgnews()
		assert len(sp)==7, f"\t test_spg FAILED"

class TestReadNews(TopicRSS, FormatTopic, ReadNews):
	@pytest.fixture(scope="class")
	def newsfx(self, Allnews): 
		return Allnews

	@pytest.fixture
	def models(self):
		return self._models()
		
	@pytest.fixture
	def topic(self):
		return Topics.get_topic_by_eng_name('sport')	

	@property
	def request(self):
		return Allnws().request

	def test_author(self):
		assert self._author(34472,'blog')=="Александр Морозов", f"\t test_news_q FAILED"
		
	def test_get_topic_news_len(self,topic,newsfx):
		assert len(self.get_topic_news_ename(topic.eng_name))==50, f"\t _get_topic_news FAILED"

	def test_format_news_phts_url(self,topic,newsfx):
		n=self.get_topic_news_ename(topic.eng_name)[0]
		assert 'https://image.' in n.image and '.jpg' in n.image and re.search(r'/v2/\d{2}/\d{4}/\d{2}/\w/[\d\w]{32}',n.image), f"\t test_format_news_phts_url FAILED"


class TestModelsNews(ModelsNews):
	@pytest.fixture
	def models(self):
		return self._models()
		
	def test_models(self,models):
		assert len(models)==9, f"\t test_models FAILED"

	def test_model(self):
		assert self.my_model('sport').eng_name=='sport', f"\t test_model FAILED"

class TestReadNews(ReadNews):
	@classmethod
	def turbo(cls):
		return True
	
	def test_regular_news_q(self):
		assert len(self._regular_news_q('sport'))==50, f"\t test_regular_news_q FAILED"

class ReadNewsTurbo:
	@classmethod
	def turbo(cls):
		raise NotImplementedError("Non Implemented turbo inherited from TestReadNewsTurbo")

	@classmethod
	def count(cls):
		raise NotImplementedError("Non Implemented count inherited from TestReadNewsTurbo")
		
	def test_news_q(self):
		assert len(self._news_q('sport'))==self.count(), f"\t test_news_q FAILED"

class TestReadNewsTurboTrue(ReadNews, ReadNewsTurbo):
	@classmethod
	def turbo(cls):
		return True

	@classmethod
	def count(cls):		
		return 114
		
class TestReadNewsTurboFalse(ReadNews, ReadNewsTurbo):
	@classmethod
	def turbo(cls):
		return False

	@classmethod
	def count(cls):		
		return 50
		
	
"""
GetNewsByUrl - getting and formatting news for spiegels 
"""
class TestGetNewsByUrl(ReadSpgHot):
	@pytest.fixture(scope="class")
	def spg_news(self):
		return ReadSpgHot().spgnews()
	
	def test_get_news(self,spg_news):
		assert self.get_one_news(spg_news[0]).url.startswith('http') and self.get_one_news(spg_news[0]).url.endswith('html') , f"\t test_format_news_phts_url FAILED"

"""
Turbo
"""
class TestTopicRssTurbo:
	@pytest.fixture(scope="class")
	def AllnwsTurbo(self):
		res = AllnewsGet()
		res.request = RequestFactory().get('yandex/turbo') 
		return res	
	
	def test_clear_title(self,AllnwsTurbo):	
		assert AllnwsTurbo.clear_title("ee xx&39;uu")=="ee xx'uu", f"\t test_clear_title FAILED"
		
	def test_turbo_news_ln_eq_1000(self,AllnwsTurbo):	
		assert len(AllnwsTurbo.allnews())==1000, f"\t test_turbo_news_ln_eq_1000 FAILED"		

''''''