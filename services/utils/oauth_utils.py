
from services.facebook_service import FacebookService


def validate_oauth_token(grant_type, token):
    if grant_type == 'facebook':
        return validate_fb_token(token)
    else:
        return False


def validate_fb_token(token):
    debug_result = FacebookService.debug_token(token)

    user_id = None
    if debug_result['data']['is_valid']:
        user_id = debug_result['data']['user_id']

    print(token)
    return {
        'user_id': user_id,
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@test.com'
    }
