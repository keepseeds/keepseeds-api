"""
Module containing the FacebookService definition.
"""
import os
import facebook
import yaml

from helpers import resource_exceptions as res_exc


class FacebookService(object):
    """
    Service for Facebook actions.
    """
    @classmethod
    def get_user_details_by_token(cls, token):
        """
        Provided with an access token, look up the user - returning
        basic details.

        :param token: Access token of user.
        :type token: str
        :rtype: dict
        """
        graph = cls.__get_graph()

        try:
            debug_result = graph.get_object('debug_token', input_token=token)
            if not debug_result['data'] or not debug_result['data']['is_valid']:
                raise res_exc.InvalidCredentialsError
        except facebook.GraphAPIError:
            raise res_exc.UnableToCompleteError

        user_result = graph.get_object(
            id=debug_result['data']['user_id'],
            fields='first_name,last_name,email'
        )
        if not user_result['email']:
            raise res_exc.FacebookInvalidPermissionsError('email')

        return user_result

    @staticmethod
    def __get_graph():
        """
        Return a new instance of the Facebook Graph API using the app creds.
        """
        app_id = os.environ.get('FACEBOOK_APP_ID')
        app_secret = os.environ.get('FACEBOOK_APP_SECRET')

        if not app_id and not app_secret:
            # No environment variables, use yaml file instead.
            with open('app_config.yml') as stream:
                try:
                    config = yaml.load(stream)
                    app_id = config['facebook_app']['app_id']
                    app_secret = config['facebook_app']['app_secret']
                except yaml.YAMLError as exc:
                    print(exc)

        return facebook.GraphAPI(
            access_token='{}|{}'.format(app_id, app_secret),
            timeout=1000,
            version='2.7'
        )
