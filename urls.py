from django.urls import path, re_path
import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.http import Http404

app_name = 'rss'

handler404 = views.Err404.as_view()
handler500 = views.Err500.as_view() 

urlpatterns = [
    re_path(r'robots\.txt$', views.Robots.as_view(), name='robots'),  
    re_path(r'top/big/?$', views.Big.as_view(), name='topbig'),
    re_path(r'top/main/?$', views.Main.as_view(), name='topmain'),    
    re_path(r'big/?$', views.Big.as_view(), name='topbg'),
    re_path(r'yandex/?$', views.Yandex.as_view(), name='yandex'),
    re_path(r'yandex/news/?$', views.Yandex.as_view(), name='yandexnews'),
    re_path(r'yandex/zen/?$', views.YandexZen.as_view(), name='yandexzen'),
    re_path(r'yandex/turbo/?$', views.YandexTurbo.as_view(), name='yandexturbo'),
    re_path(r'interfax/?$', views.Interfax.as_view(), name='interfax'),
    re_path(r'mail/?$', views.Mail.as_view(), name='mail'),
    re_path(r'rambler/?$', views.Rambler.as_view(), name='rambler'),
	re_path(r'all_news/?$', views.AllnewsGet.as_view(), name='allnews'),
	re_path(r'all/?$', views.AllnewsGet.as_view(), name='all'),	
    re_path(r'google/all_news/?$', views.GoogleAll.as_view(), name='Google_allnews'),
	re_path(r'google/all/?$', views.GoogleAll.as_view(), name='Google_all'),
	re_path(r'google/(?P<eng_name>russia|world|finance|cinema|sport|auto|blog|hitech|realty)/?$', views.Google.as_view(), name='google'),
    re_path(r'facebook/?$', views.Facebook.as_view(), name='facebook'),
    re_path(r'fbinstant/?$', views.Facebook.as_view(), name='facebookinst'),
    re_path(r'favicon.ico', RedirectView.as_view(url="https://static.newsru.com/static/v3/img/icons/favicon.ico")),
    re_path(r'404.html', views.Err404.as_view(), name='err404'),
    re_path(r'500.html', views.Err500.as_view(), name='err500'),  
    re_path(r'^(?P<eng_name>russia|world|finance|cinema|sport|auto|blog|hitech|realty)/?$', views.TopicGet.as_view(), name='topic'),
    re_path(r'.*', views.Err404.as_view(), name='404'),]
 
