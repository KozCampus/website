from __future__ import annotations

from uuid import UUID

from kc.exceptions import *


class TokenMissingError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """No authentication token was sent to the server."""


class TokenInvalidError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """The provided authentication token is invalid."""


class AccountNotFoundError(Error, status_code=HTTP_404_NOT_FOUND):
    """The requested account was not found."""


class InvalidPasswordError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """The provided password is invalid."""


class TOTPError(Error, status_code=HTTP_400_BAD_REQUEST):
    """TOTP verification failed."""


class ForbiddenError(Error, status_code=HTTP_403_FORBIDDEN):
    """The client is not authorized to perform this action."""


class NoPasswordSetError(Error, status_code=HTTP_409_CONFLICT):
    """This user has no password set. Contact administrators."""


class NotOrganizerError(Error, status_code=HTTP_403_FORBIDDEN):
    """This user has no organizer account set up."""


class NotParticipantError(Error, status_code=HTTP_403_FORBIDDEN):
    """This user has no participant account set up. Register as a participant on the homepage."""


class NotSpeakerError(Error, status_code=HTTP_403_FORBIDDEN):
    """This user has no speaker account set up."""
