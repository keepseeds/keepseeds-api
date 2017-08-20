"""
Module containing custom field definitions for marshals.
"""
from flask_restful import fields

ISODate = fields.DateTime(dt_format='iso8601')
