from marshmallow.fields import Str, Date, Int

put_child_args = {
    'first_name': Str(),
    'last_name': Str(),
    'date_of_birth': Date(),
    'gender_id': Int(),
    'middle_name': Str()
}
