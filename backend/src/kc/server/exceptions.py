from __future__ import annotations

from uuid import UUID

from kc.exceptions import *


class TokenMissingError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """No authentication token was sent to the server."""


class TokenInvalidError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """The authentication token is invalid."""


class AccountNotFoundError(Error, status_code=HTTP_404_NOT_FOUND):
    """The account was not found."""


class InvalidPasswordError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """The provided password is invalid."""


class TOTPError(Error, status_code=HTTP_400_BAD_REQUEST):
    """TOTP verification failed."""


class ForbiddenError(Error, status_code=HTTP_403_FORBIDDEN):
    """The client is not authorized to perform this action."""


class NoPasswordSetError(Error, status_code=HTTP_409_CONFLICT):
    """The account requested has no password set. Contant administrators."""


class NotOrganizerError(Error, status_code=HTTP_403_FORBIDDEN):
    """The account requested has no organizer account set up."""


class NotParticipantError(Error, status_code=HTTP_403_FORBIDDEN):
    """The account requested has no participant account set up. Register as an participant on the homepage."""


class NotSpeakerError(Error, status_code=HTTP_403_FORBIDDEN):
    """The account requested has not speaker account set up."""
