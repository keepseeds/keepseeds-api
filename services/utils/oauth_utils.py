
def validate_oauth_token(grant_type, token):
    if grant_type == 'facebook':
        return validate_fb_token(token)
    else:
        return False

def validate_fb_token(token):
    print(token)
    return {
        'user_id': 20001,
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@test.com'
    }
