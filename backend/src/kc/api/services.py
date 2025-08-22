from __future__ import annotations

from kc.contrib.litestar import SQLAlchemyAsyncRepositoryService
from kc.models import *
from kc.api.repositories import *


class AccountService(SQLAlchemyAsyncRepositoryService[Account]):
    repository_type = AccountRepository
