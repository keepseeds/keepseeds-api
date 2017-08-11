"""
Module containing custom field definitions for marshallers.
"""
from flask_restful import fields

ISODate = fields.DateTime(dt_format='iso8601')
