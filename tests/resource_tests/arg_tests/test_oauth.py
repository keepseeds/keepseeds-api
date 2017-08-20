from resources.args.oauth import post_oauth_args

"""
{
    'email': Str(required=True),
    'password': Str(required=True)
}
"""
def test__post_oauth_args__keys():
    assert len(post_oauth_args.keys()) == 2
    assert 'grant_type' in post_oauth_args.keys()
    assert 'token' in post_oauth_args.keys()
