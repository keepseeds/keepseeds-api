from resources.args.verify_email import post_verify_email_args

"""
{
    'email': Str(required=True),
    'token': Str(required=True)
}
"""
def test__post_verify_email_args__keys():
    assert len(post_verify_email_args.keys()) == 2
    assert 'email' in post_verify_email_args.keys()
    assert 'token' in post_verify_email_args.keys()
