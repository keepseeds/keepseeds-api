from resources._args.child import put_child_args

"""
{
    'first_name': Str(),
    'last_name': Str(),
    'date_of_birth': Date(),
    'gender': Int(),
    'middle_name': Str()
}
"""
def test__put_child_args__keys():
    assert len(put_child_args.keys()) == 5
    assert 'first_name' in put_child_args.keys()
    assert 'last_name' in put_child_args.keys()
    assert 'date_of_birth' in put_child_args.keys()
    assert 'gender' in put_child_args.keys()
    assert 'middle_name' in put_child_args.keys()
