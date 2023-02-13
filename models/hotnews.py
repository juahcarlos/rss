from mongoengine import *

class Hotnews(Document):
    hotnews_id = IntField()
    title = StringField(max_length=255)
    url = StringField(max_length=255)
    date_create = DateTimeField()
    date_modify = DateTimeField()
    editor_id = IntField()
    position = IntField()
    meta = {"db_alias":"default"}    

    @classmethod
    def findall(cls):
        return cls.objects().order_by('+position').limit(4)