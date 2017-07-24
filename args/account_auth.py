from marshmallow.fields import Str

post_account_auth_args = {
    "email": Str(required=True),
    "password": Str(required=True)
}
