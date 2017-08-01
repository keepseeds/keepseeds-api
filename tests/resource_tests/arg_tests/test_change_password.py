from resources.args.change_password import put_change_password_args

def test__put_change_password_args__keys():
    assert len(put_change_password_args.keys()) == 3
    assert 'oldPassword' in put_change_password_args.keys()
    assert 'password' in put_change_password_args.keys()
    assert 'passwordConfirm' in put_change_password_args.keys()
