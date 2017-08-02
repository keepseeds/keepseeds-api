
from services.facebook_service import FacebookService


def validate_oauth_token(grant_type, token):
    if grant_type == 'facebook':
        return validate_fb_token(token)
    else:
        return False


def validate_fb_token(token):
    user_detail = FacebookService.get_user_details_by_token(token)

    return {
        'user_id': user_detail['id'],
        'first_name': user_detail['first_name'],
        'last_name': user_detail['last_name'],
        'email': user_detail['email']
    }
