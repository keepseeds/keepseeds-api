from marshmallow.fields import Str

put_change_password_args = {
    'email': Str(required=True),
    'oldPassword': Str(required=True),
    'password': Str(required=True),
    'passwordConfirm': Str(required=True)
}
