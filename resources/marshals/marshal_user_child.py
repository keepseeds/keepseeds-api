from flask_restful import fields

# For producing a list of children for a specific user.
list_users_children = {
    'id': fields.Integer(attribute='child.id'),
    'first_name': fields.String(attribute='child.first_name'),
    'last_name': fields.String(attribute='child.last_name'),
    'middle_name': fields.String(attribute='child.middle_name'),
    'gender_id': fields.Integer(attribute='child.gender_id'),
    'date_of_birth': fields.DateTime(attribute='child.date_of_birth', dt_format='iso8601'),
    'has_ownership': fields.Boolean(attribute='is_primary')
}
