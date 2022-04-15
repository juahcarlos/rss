from mongoengine import *
from logger import *

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
	is_index = IntField()
	meta = {"db_alias":"default"}
	
	@classmethod
	def topics_main_menu(cls):
		res = cls.objects( Q(is_main_menu=1) & Q(eng_name__nin=['promo','crime','religy']) )
		return res

	@classmethod
	def get_topic_by_eng_name(cls,eng_name):
		res = cls.objects(eng_name=eng_name).first()
		return res