from __future__ import annotations

from litestar import Request
from litestar.connection import ASGIConnection
from litestar.handlers import BaseRouteHandler

from kc.contrib.litestar import *
from kc.api.services import *
from kc.api.auth import decode_token, Claims, get_claims_from_cookies
from kc.api.exceptions import *
from kc.api import get_session, get_settings


def get_dependencies() -> dict[str, Provide]:
    return {
        "claims": Provide(provide_claims),
        "account": Provide(provide_account),
        "account_service": Provide(provide_account_service),
    }


async def provide_claims(
    request: Request,
) -> Claims | None:
    return get_claims_from_cookies(request.cookies)


async def require_admin(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    claims = get_claims_from_cookies(connection.cookies)
    if claims is None:
        raise TokenMissingError()

    async with get_session() as session:
        async with AccountService.new(session) as account_service:
            account = await account_service.get_one_or_none(id=claims.sub)

    if account is None:
        raise AccountNotFoundError()

    if not account.is_admin:
        raise AdminRequiredError()


async def provide_account(
    account_service: AccountService,
    claims: Claims,
) -> Account:
    db_obj = await account_service.get_one_or_none(id=claims.sub)

    if not db_obj:
        raise AccountNotFoundError()
    
    return db_obj


provide_account_service = create_service_provider(AccountService)
