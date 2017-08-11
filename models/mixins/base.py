"""
Base module for Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

from db import db


class Base(object):
    """
    Base Mixin, provides:
    id, create_date_time, update_date_time and delete_date_time
    """
    id = Column(Integer, primary_key=True)
    create_date_time = Column(DateTime, default=datetime.utcnow)
    update_date_time = Column(DateTime, onupdate=datetime.utcnow)
    delete_date_time = Column(DateTime)

    @staticmethod
    def save():
        db.session.commit()

    @classmethod
    def add(cls, new_object, is_save=True):
        db.session.add(new_object)

        if is_save:
            cls.save()
