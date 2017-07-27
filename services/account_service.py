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
        """Register a new user."""

        if User.find_by_email(email):
            raise res_exc.EmailAlreadyExistsError(email)

        validate_password(password, password_confirm)

        create_user_result = User.create(email, first, last, password)

        return create_user_result

    def verify_email(self, email, token):
        """Verify an email address for a user."""

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
        """Change the password for a user."""

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
        """Request a password reset for a user."""
        user = User.find_by_email(email)

        if not user:
            raise res_exc.UserNotFoundError

        token = Token.find_by_token_type(TokenType.ResetPassword)

        if not token:
            raise res_exc.UnableToCompleteError

        new_user_token_id = UserToken.create(user, token)

        return {'userTokenId': new_user_token_id}

    def resolve_password_reset(self, email, password, password_confirm, token):
        """Resolve a password reset for a user."""
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
        """Authenticate a user."""
        user = User.find_by_email(email)

        if not user or not user.verify_password(password):
            raise res_exc.InvalidCredentialsError

        if not user.is_verified_email:
            raise res_exc.EmailNotVerifiedError

        return self.__get_access_token(user.id)

    def oauth_authentication(self, grant_type, token):
        if not grant_type in ('facebook',):
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
        """
        return {'accessToken': create_access_token(identity=identifier)}
