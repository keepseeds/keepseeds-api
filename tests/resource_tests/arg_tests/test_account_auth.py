from resources._args.account_auth import post_account_auth_args

"""
{
    'email': Str(required=True),
    'password': Str(required=True)
}
"""
def test__post_account_auth_args__keys():
    assert len(post_account_auth_args.keys()) == 2
    assert 'email' in post_account_auth_args.keys()
    assert 'password' in post_account_auth_args.keys()
