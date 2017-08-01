"""
Module containing the FacebookService definition.
"""
import facebook

class FacebookService(object):

    @classmethod
    def debug_token(cls, token):
        app_id = ''
        app_secret = ''
        graph = facebook.GraphAPI(
            access_token='{}|{}'.format(app_id, app_secret),
            timeout=1000,
            version='2.7'
        )

        return graph.get_object('debug_token', input_token=token)

