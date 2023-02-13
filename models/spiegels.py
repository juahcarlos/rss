from mongoengine import *
import re
import datetime
from dateutil.parser import *
from dateutil.tz import *
from dateutil.relativedelta import *


class Spiegels(Document):
    spiegel_id = IntField()
    title = StringField(max_length=255)
    text = StringField(max_length=255)
    url = StringField(max_length=255)
    date_create = DateTimeField()
    date_modify = DateTimeField()
    editor_id = IntField()
    position = IntField()
    is_rotate = IntField()
    old_id = IntField()
    meta = {"db_alias":"default"} 

    @classmethod
    def findall(cls):
        spiegels = cls.objects( Q(position__gt=0) & Q(position__lt=4) ).order_by('+position').all()
        return spiegels

    @classmethod
    def find_by_pos(cls,pos):
        res = cls.objects(position=pos).first()
        return res