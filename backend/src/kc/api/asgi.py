from __future__ import annotations

from litestar.middleware.rate_limit import RateLimitConfig

from kc.api import factory
from kc.api.dependencies import get_dependencies
from kc.api.routes import get_routes

routes = get_routes()
factory.add_routes(routes)

dependencies = get_dependencies()
factory.add_dependencies(dependencies)

minute_rate_limit = RateLimitConfig(("minute", 100))
hourly_rate_limit = RateLimitConfig(("hour", 1000))
daily_rate_limit = RateLimitConfig(("day", 5000))

factory.add_middleware(minute_rate_limit.middleware)
factory.add_middleware(hourly_rate_limit.middleware)
factory.add_middleware(daily_rate_limit.middleware)

app = factory.create_app()
