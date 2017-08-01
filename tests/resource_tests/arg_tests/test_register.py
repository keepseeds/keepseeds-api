from resources.args.register import post_register_args

"""
{
    'firstName': Str(required=True),
    'lastName': Str(required=True),
    'email': Str(required=True),
    'password': Str(required=True),
    'passwordConfirm': Str(required=True)
}
"""
def test__post_register_args__keys():
    assert len(post_register_args.keys()) == 5
    assert 'firstName' in post_register_args.keys()
    assert 'lastName' in post_register_args.keys()
    assert 'email' in post_register_args.keys()
    assert 'password' in post_register_args.keys()
    assert 'passwordConfirm' in post_register_args.keys()
