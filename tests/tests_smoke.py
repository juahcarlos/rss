import pytest
import requests

@pytest.fixture()
def urls():
	urls = [
		'/top/main/',
		'/top/big/',
		'/sport/',
		'/all_news/',
		'/google/world/',
		'/yandex/',
		'/yandex/turbo/',
		'/facebook/',
	]
	host = 'http://82.165.223.38:8021'
	res = list(map(lambda x: host + x, urls))
	return  res



def test_head(urls):
	for u in urls:
		r = requests.head(u)
		assert r.status_code==200, f"\t{u} {r.status_code}"
		

def test_get(urls):
	len_limit = 5000
	for u in urls:
		r = requests.get(u)
		assert r.status_code==200, f"\t{u} {r.status_code}"
		assert len(r.text)>len_limit, f"\t{u} lower {len_limit}"
