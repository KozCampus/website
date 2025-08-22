from __future__ import annotations

from kc.cli import create_cli

cli = create_cli("kc.api.asgi:app")


if __name__ == "__main__":
    cli()
