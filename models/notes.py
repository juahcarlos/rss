from mongoengine import *

class Notes(Document):
    note_id = IntField()
    rus_name = StringField(max_length=255)
    date_create = DateTimeField()
    date_modify = DateTimeField()
    note_types_id = IntField()
    parent_id = IntField()
    count = IntField()

    @classmethod
    def note_by_id(cls,id):
        res = cls.objects(note_id=id).limit(1)
        if res:
            return res[0]
        return

    @classmethod
    def note_by_rus_name(cls,name):
        res = cls.objects(Q(rus_name=name) & Q(parent_id=0) )
        if res:
            return res
        return

    @classmethod
    def note_by_parent_id_rubrick(cls):
        #pr_ids = cls.note_by_rus_name(rus_name)
        res = cls.objects( rus_name='Рубрики' ).all()
        if res:
            return res
        return

    @classmethod
    def notes_for_splashka(cls,rus_names):
        ids = []
        for iq in cls.note_by_parent_id_rubrick():
            ids.append(iq.note_id)
        res = cls.objects( Q(parent_id__in=ids) & Q(rus_name__in=rus_names) ).order_by('+rus_name').all()
        return res        

    @classmethod
    def notes_by_id(cls,id,limit=None):
        if limit:
            return cls.objects(parent_id=id).order_by('+rus_name').limit(limit)
        res = cls.objects(parent_id=id).order_by('+rus_name')
        return res

    @classmethod
    def parent_by_id(cls,prnt_id):
        res = cls.objects( Q(note_id=prnt_id) ).limit(1)
        if res:
            return res[0]
        else:
            return None

    @classmethod
    def notes_by_type(cls,id):
        res = cls.objects( Q(note_types_id=id) & Q(parent_id=0) ).order_by('+rus_name')
        return res

    @classmethod
    def update_count(cls,id,cnt):
        try:
            cls.objects(note_id=id).update_one(set__count=cnt)
        except Exception as ex:
            return 'cant update notes count note_id={} count={} ex={}'.format(note_id,count,ex)
        return 
