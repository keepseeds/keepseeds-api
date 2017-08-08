
from db import db

class BaseService(object):

    @staticmethod
    def save():
        db.session.commit()

    @classmethod
    def add(cls, new_entity, is_save=False):
        db.session.add(new_entity)

        if is_save:
            cls.save()
