
from flask_restful import fields
from resources.marshals import custom_fields

# For a single child, return all relevant fields.
single_child_marshal = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'middle_name': fields.String,
    'date_of_birth': custom_fields.ISODate,
    'gender_id': fields.Integer,
    'created_by': fields.Integer,
    'create_date_time': custom_fields.ISODate,
    'update_date_time': custom_fields.ISODate
}

# For a list of children, just return basic information.
list_child_marshal = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'middle_name': fields.String,
    'gender_id': fields.Integer,
}
