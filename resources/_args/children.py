from marshmallow.fields import Str, Date, Int

post_children_args = {
    'first_name': Str(required=True),
    'last_name': Str(required=True),
    'date_of_birth': Date(required=True),
    'gender_id': Int(required=True),
    'middle_name': Str()
}
