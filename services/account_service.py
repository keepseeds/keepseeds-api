"""Module containing the AccountService definition."""

from flask_jwt_extended import get_jwt_identity

from models import User, Token, UserToken
from models.enums import TokenType
from helpers import resource_exceptions as res_exc
from .utils import get_access_token, validate_password


class AccountService(object):
    """
    Service for account actions.
    """
    @classmethod
    def register_user(cls, email, first, last, password, password_confirm):
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

    @staticmethod
    def verify_email(email, token):
        """
        Verify an email address for a user.

        :param email: User's email address.
        :type email: str
        :param token: Temporary token to authenticate with.
        :type token: str
        :rtype: bool
        """

        # Lookup user via email.
        user = User.find_by_email(email)

        if not user:
            raise res_exc.UserNotFoundError

        # Lookup user token with the id of the user and token type.
        user_token = UserToken.find_by_user_and_type(
            user_id=user.id,
            token_type=TokenType.VerifyEmail)

        if not user_token or not user_token.verify_token(token):
            raise res_exc.InvalidTokenError(token)

        # Update user to set is_verified_email=True
        if not user.set_is_verified_email():
            raise res_exc.UnableToCompleteError

        # Expire this user token and return True.
        user_token.expire()
        return True

    @classmethod
    def change_password(cls, old_password, password, password_confirm):
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

        user = User.find_by_id(get_jwt_identity())

        if not user:
            raise res_exc.UserNotFoundError

        if not user.verify_password(old_password):
            raise res_exc.UnableToCompleteError

        validate_password(password, password_confirm)

        if not user.update_password(password):
            raise res_exc.UnableToCompleteError

        return True

    @staticmethod
    def request_password_reset(email):
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

        if not new_user_token_id:
            raise res_exc.UnableToCompleteError

        return {'userTokenId': new_user_token_id}

    @classmethod
    def resolve_password_reset(cls, email, password, password_confirm, token):
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

        user_token = UserToken.find_by_user_and_type(
            user_id=user.id,
            token_type=TokenType.ResetPassword)

        if not user_token or not user_token.verify_token(token):
            raise res_exc.InvalidTokenError(token)

        validate_password(password, password_confirm)

        if not user.update_password(password):
            raise res_exc.UnableToCompleteError

        user_token.expire()
        return True

    @classmethod
    def authenticate_user(cls, email, password):
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
            raise res_exc.EmailNotVerifiedError(email)

        return get_access_token(user.id)

    @staticmethod
    def authenticate_oauth(grant_type, token):
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
