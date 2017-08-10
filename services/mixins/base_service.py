
from db import db

class BaseService(object):

    @staticmethod
    def save():
        """
        Commit changes to the current session.

        :return:
        """
        db.session.commit()

    @classmethod
    def add(cls, new_entity, is_save=False):
        """
        Add entity and call save() if is_save.

        :param new_entity:
        :param is_save:
        :return:
        """
        db.session.add(new_entity)

        if is_save:
            cls.save()
