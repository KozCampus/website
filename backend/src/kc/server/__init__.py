from __future__ import annotations

from kc.contrib.litestar import AppFactory
from kc.server.settings import Settings

factory = AppFactory(Settings, lambda settings: settings)

get_settings = factory.create_settings_getter()
get_session = factory.create_session_getter()
