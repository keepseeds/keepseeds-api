"""Module containing the AccountService definition."""
from flask_jwt_extended import create_access_token

from models import User, Token, UserToken
from models.enums import TokenType
from helpers import resource_exceptions as res_exc, validate_password


class AccountService(object):
    """
    Service for account actions.
    """
    def register_user(self, email, first, last, password, password_confirm):
        """
        Register a new user.

        :param email: New user's email address.
        :type email: str
        :param first: New user's first name.
        :type first: str
        :param last: New user's last name.
        :type last: str
        :param password: New user's password.
        :type password: str
        :param password_confirm: New user's password confirmation.
        :type password_confirm: str
        :rtype: str
        """

        if User.find_by_email(email):
            raise res_exc.EmailAlreadyExistsError(email)

        validate_password(password, password_confirm)

        create_user_result = User.create(email, first, last, password)

        return create_user_result

    def verify_email(self, email, token):
        """
        Verify an email address for a user.

        :param email: User's email address.
        :type email: str
        :param token: Temporary token to authenticate with.
        :type token: str
        :rtype: bool
        """

        user = User.find_by_email(email)

        if not user:
            raise res_exc.UserNotFoundError

        vtr = UserToken.validate_token(user.id, token, TokenType.VerifyEmail)

        if not vtr.is_valid:
            raise res_exc.InvalidTokenError(token)

        if user.set_is_verified_email(email):
            vtr.user_token.expire()

        return True

    def change_password(self, email, old_password, password, password_confirm):
        """
        Change the password for a user.

        :param email: User's email.
        :type email: str
        :param old_password: User's current password, to be changed.
        :type old_password: str
        :param password: User's new password.
        :type password: str
        :param password_confirm: Confirmation of the User's new password.
        :type password_confirm: str
        :rtype: bool
        """

        user = User.find_by_email(email)

        if not user:
            raise res_exc.UserNotFoundError

        if not user.verify_password(old_password):
            raise res_exc.UnableToCompleteError

        validate_password(password, password_confirm)

        if not User.update_password(email, password):
            raise res_exc.UnableToCompleteError

        return True

    def request_password_reset(self, email):
        """
        Request a password reset for a user.

        :param email: Email address of user to send password reset email.
        :type email: str
        :rtype: dict
        """
        user = User.find_by_email(email)

        if not user:
            raise res_exc.UserNotFoundError

        token = Token.find_by_token_type(TokenType.ResetPassword)

        if not token:
            raise res_exc.UnableToCompleteError

        new_user_token_id = UserToken.create(user, token)

        return {'userTokenId': new_user_token_id}

    def resolve_password_reset(self, email, password, password_confirm, token):
        """
        Resolve a password reset for a user.

        :param email: User's email address to reset password.
        :type email: str
        :param password: New password for user.
        :type password: str
        :param password_confirm: Confirmation of user's new password.
        :type password_confirm: str
        :param token: User's email token to authenticate with.
        :type token: str
        :rtype: dict
        """
        user = User.find_by_email(email)

        if not user:
            raise res_exc.UserNotFoundError

        vr = UserToken.validate_token(user_id=user.id,
                                      token=token,
                                      token_type=TokenType.ResetPassword)

        if not vr.is_valid:
            raise res_exc.InvalidTokenError

        validate_password(password, password_confirm)

        if User.update_password(email, password):
            vr.user_token.expire()
            return {'message': 'Done.'}

        raise res_exc.UnableToCompleteError

    def authenticate_user(self, email, password):
        """
        Authenticate a user.

        :param email: User's email address to identify user.
        :type email: str
        :param password: User's plain-text password.
        :type password: str
        :rtype: dict
        """
        user = User.find_by_email(email)

        if not user or not user.verify_password(password):
            raise res_exc.InvalidCredentialsError

        if not user.is_verified_email:
            raise res_exc.EmailNotVerifiedError

        return self.__get_access_token(user.id)

    def oauth_authentication(self, grant_type, token):
        """
        Authenticate a user via OAuth.

        :param grant_type: Type of OAuth authentication to validate against.
        :type grant_type: str
        :param token: Authentication token provided by provider.
        :type token: str
        :rtype: dict
        """
        if grant_type not in ('facebook',):
            raise res_exc.InvalidCredentialsError

        # 1. Ensure we support grantType provided
        # 2. Look up user based on token via 3rd party, ensure the access token
        #    belongs to our app and they have granted required permissions.
        # 3. Look up user id locally in user_grants.
        # 4. If the user doesn't exist we need to create it and get the id.
        # 5. Finally, return an access token using get_access_token and our
        #    local user id.

        raise NotImplementedError

    def __get_access_token(self, identifier):
        """
        [PRIVATE] Generate and return an access token using the
        provided identifier.

        :param identifier: Unique id to identify this user.
        :rtype: dict
        """
        return {'accessToken': create_access_token(identity=identifier)}
