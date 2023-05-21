from dependency_injector import containers, providers
from fastapi import FastAPI

from .settings import FastAPISettings


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize common FastAPI dependencies.

    Important that there we do not configure and wire Container. It is done in FastAPI
    factory function in app.api.main module.

    Args:
        app (FastAPI): to bootstrap with global dependencies.

    Returns:
        FastAPI: bootstrapped with global dependencies.
    """
    return app


class Container(containers.DeclarativeContainer):
    """Container for dependencies used in API presentation layer.

    Highly suggested to use Object provider for BaseSettings as Configuration provider
    just looses all typing, validation and logic that might be the part of settings.

    When some dependency must be configured at startup use Abstract dependencies and
    override them on application startup.
    """

    fastapi_settings = providers.Object(FastAPISettings())
