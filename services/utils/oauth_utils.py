from services.facebook_service import FacebookService


def validate_oauth_token(grant_type, token):
    if grant_type == 'facebook':
        return FacebookService.get_user_details_by_token(token)
    else:
        return False
