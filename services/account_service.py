"""Module containing the AccountService definition."""

from models import User, UserToken
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

    def request_password_reset(self):
        """Request a password reset for a user."""
        pass

    def resolve_password_reset(self):
        """Resolve a password reset for a user."""
        pass

    def authenticate_user(self):
        """Authenticate a user."""
        pass
