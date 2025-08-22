from __future__ import annotations

from kc.contrib.litestar import SQLAlchemyAsyncRepository
from kc.models import *


class AccountRepository(SQLAlchemyAsyncRepository[Account]):
    model_type = Account
