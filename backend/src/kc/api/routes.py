from __future__ import annotations

import typing as t

from litestar import Request, Response
from litestar.middleware.rate_limit import RateLimitConfig

from kc.contrib.litestar import *
from kc.api.exceptions import *
from kc.api.schemas import *
from kc.api.services import *
from kc.api.auth import *
from kc.api.dependencies import require_admin


def get_routes() -> list[ControllerRouterHandler]:
    return [
        AuthController,
        AccountController,
    ]


auth_minute_rate_limit = RateLimitConfig(("minute", 60))
auth_daily_rate_limit = RateLimitConfig(("day", 600))


def set_auth_cookie(
    response: Response,
    token: str,
) -> None:
    settings = get_settings()

    if settings.api.debug:
        response.set_cookie(
            key="Auth",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=JWT_LIFETIME,
        )
    else:
        response.set_cookie(
            key="__Secure-Auth",
            value=token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=JWT_LIFETIME,
        )


class AuthController(Controller):
    path = "/auth"
    tags = ["Auth"]
    middleware = [
        auth_minute_rate_limit.middleware,
        auth_daily_rate_limit.middleware,
    ]


    @post(
        operation_id="LoginClient",
        path="/login",
    )
    async def login_client(
        self,
        data: ClientLogin,
        account_service: AccountService,
    ) -> Response:
        account = await account_service.get_one_or_none(email=data.email)
        if account is None:
            raise AccountNotFoundError()
        
        if not verify_password(
            plain=data.password, 
            hashed=account.password_hash,
        ):
            raise InvalidPasswordError()
        
        if account.is_banned:
            raise AccountBannedError(account_id=account.id)
        
        claims = create_claims(
            account_id=account.id,
            account_read=True,
            account_write=True,
        )

        token = issue_token(claims)
        
        response = Response(content=None, status_code=204)
        set_auth_cookie(response, token)

        return response


    @get(
        operation_id="GetClientClaims",
        path="/claims",
    )
    async def get_client_claims(
        self,
        claims: Claims | None,
    ) -> Claims | None:
        return claims
    

    @post(
        operation_id="SetupClientTOTP",
        path="/setup-totp",
    )
    async def setup_client_totp(
        self,
        account: Account,
        account_service: AccountService,
    ) -> TOTPSchema:
        schema = issue_totp_secret(account.name)
        try:
            encrypted_secret = encrypt_totp_secret(schema.secret)
            await account_service.update(
                item_id=account.id,
                data={"encrypted_totp_secret": encrypted_secret},
            )
        except:
            import traceback
            traceback.print_exc()
        return schema


class AccountController(Controller):
    path = "/accounts"
    tags = ["Accounts"]


    @get(
        operation_id="ListAccounts",
        path="",
        cache=60,
        guards=[require_admin],
    )
    async def list_accounts(
        self,
        account_service: AccountService,
        filters: t.Annotated[
            list[FilterTypes],
            Dependency(skip_validation=True),
        ]
    ) -> OffsetPagination[AccountSchema]:
        results, total = await account_service.list_and_count(*filters)
        return account_service.to_schema(
            data=results,
            total=total,
            schema_type=AccountSchema,
            filters=filters,
        )
    

    @get(
        operation_id="GetAccount",
        path="/{account_id:uuid}",
        guards=[require_admin],
    )
    async def get_account(
        self,
        account_id: UUID,
        account_service: AccountService,
    ) -> AccountSchema:
        db_obj = await account_service.get(account_id)
        return account_service.to_schema(
            data=db_obj,
            schema_type=AccountSchema,
        )
    

    @get(
        operation_id="GetClientAccount",
        path="/me",
    )
    async def get_client_account(
        self,
        account: Account,
        account_service: AccountService,
    ) -> AccountSchema:
        return account_service.to_schema(
            data=account,
            schema_type=AccountSchema,
        )
    

    @delete(
        operation_id="DeleteAccount",
        path="/{account_id:uuid}",
        guards=[require_admin],
    )
    async def delete_account(
        self,
        account_id: UUID,
        account_service: AccountService,
    ) -> None:
        await account_service.delete(account_id)


    @post(
        operation_id="RegisterAccount",
        path="/register",
        rate_limit=RateLimitConfig(("hour", 10)),
    )
    async def register_account(
        self,
        data: AccountRegister,
        account_service: AccountService,
    ) -> Response:
        if await account_service.get_one_or_none(email=data.email):
            raise ConflictError()
        
        password_hash = hash_password(data.password)

        obj = AccountCreate(
            name=data.name,
            email=data.email,
            password_hash=password_hash,
        )

        account = await account_service.create(data=obj)
        
        claims = create_claims(
            account_id=account.id,
            account_read=True,
            account_write=True,
        )
        
        token = issue_token(claims)
        
        response = Response(content=None, status_code=204)
        set_auth_cookie(response, token)

        return response
