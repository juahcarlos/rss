import pytest
import  os
os.environ["PATH"] += os.pathsep + '/opt/web/conf'
os.environ["PATH"] += os.pathsep + '/opt/web/rss'
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'
#print(os.environ)
#exit(0)

import requests
import sys
sys.path.append('/opt/web/conf')
sys.path.append('/opt/web/rss')

from django.test import RequestFactory
from views import *

		
def test_404():
	view = Err404.as_view()
	request = RequestFactory().get('/') 
	response = view(request)
	assert response.status_code == 404		

def test_view():
	view = AllnewsGet.as_view()
	request = RequestFactory().get('all') 
	response = view(request,'allnews')
	assert response.status_code == 200

#def test_allnews():
#	r=AllnewsGet().get(request,eng_name)
#	assert r.status_code==200, f"\t{u} {r.status_code}"

