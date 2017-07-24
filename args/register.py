from marshmallow.fields import Str

post_register_args = {
    'firstName': Str(required=True),
    'lastName': Str(required=True),
    'email': Str(required=True),
    'password': Str(required=True),
    'passwordConfirm': Str(required=True)
}
