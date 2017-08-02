"""
Module containing the FacebookService definition.
"""
import os
import facebook
import yaml

class FacebookService(object):
    """
    Service for Facebook actions.
    """
    @staticmethod
    def __get_graph():
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

        debug_result = graph.get_object('debug_token', input_token=token)
        if not debug_result['data'] or not debug_result['data']['is_valid']:
            print(debug_result)
            raise Exception()

        user_id = debug_result['data']['user_id']

        user_result = graph.get_object(
            id=user_id,
            fields='first_name,last_name,email'
        )

        return user_result
