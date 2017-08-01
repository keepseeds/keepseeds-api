from resources.args.reset_password import post_reset_password_args, put_reset_password_args

def test__post_reset_password_args__keys():
    assert len(post_reset_password_args.keys()) == 4
    assert 'email' in post_reset_password_args.keys()
    assert 'token' in post_reset_password_args.keys()
    assert 'password' in post_reset_password_args.keys()
    assert 'passwordConfirm' in post_reset_password_args.keys()

def test__put_reset_password_args__keys():
    assert len(put_reset_password_args.keys()) == 1
    assert 'email' in put_reset_password_args.keys()
