from __future__ import annotations

from uuid import UUID

from kc.exceptions import *


class ClientInformationMissingError(Error, status_code=HTTP_500_INTERNAL_SERVER_ERROR):
    """Client information is not accessible."""


class TokenMissingError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """No authentication token was sent to the server."""


class TokenInvalidError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """The authentication token is invalid."""


class AccountNotFoundError(Error, status_code=HTTP_404_NOT_FOUND):
    """The account was not found."""


class InvalidPasswordError(Error, status_code=HTTP_401_UNAUTHORIZED):
    """The provided password is invalid."""


@dataclass
class AccountBannedError(Error, status_code=HTTP_403_FORBIDDEN):
    """This account is banned from using the service."""

    account_id: UUID


class VPNAPIError(Error, status_code=HTTP_500_INTERNAL_SERVER_ERROR):
    """The VPN API is not reachable. Try again later."""


class AdminRequiredError(Error, status_code=HTTP_403_FORBIDDEN):
    """The client must be an admin for this operation."""


class TOTPError(Error, status_code=HTTP_400_BAD_REQUEST):
    """TOTP verification failed."""


class TOTPDisabledError(Error, status_code=HTTP_400_BAD_REQUEST):
    """TOTP is disabled for this account."""
