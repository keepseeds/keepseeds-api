"""
Base module for Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime


class Base(object):
    """
    Base Mixin, provides:
    id, create_date_time, update_date_time and delete_date_time
    """
    id = Column(Integer, primary_key=True)
    create_date_time = Column(DateTime, default=datetime.utcnow)
    update_date_time = Column(DateTime, onupdate=datetime.utcnow)
    delete_date_time = Column(DateTime)
