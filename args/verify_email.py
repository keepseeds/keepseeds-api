from marshmallow.fields import Str

post_verify_email_args = {
    'email': Str(required=True),
    'token': Str(required=True)
}
