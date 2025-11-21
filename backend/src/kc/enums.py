from __future__ import annotations

from enum import StrEnum


class RegistrationPolicy(StrEnum):
    CLOSED = "closed"
    REQUIRED = "required"
    OPEN = "open"
