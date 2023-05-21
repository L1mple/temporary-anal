from dependency_injector import providers
from fastapi import FastAPI
from toolz import pipe

from app.service.postgres.commit.vault import CommitPostgresVault
from app.service.postgres.common.database import AsyncDb

from .analytics import endpoints as test_endpoints
from .common import dependencies, endpoints, error_handlers, event_handlers, middleware


def bootstrap() -> FastAPI:
    """Factory function for FastAPI."""
    # Initialize dependency container
    container = dependencies.Container(
        # Abstract dependencies are configured via override or arguments for Container
        # constructor
    )
    container.postgres_db.override(
        providers.Singleton(
            AsyncDb,
            db_url=container.postgres_settings.provides.get_database_url(),
            debug=container.fastapi_settings.provided.DEBUG,
        )
    )
    container.commit_repository.override(
        providers.Factory(
            CommitPostgresVault,
            db_session=container.postgres_db.provided.session,
        )
    )
    # Wire package and modules - API only as this is the only place where dependencies
    # are injected
    container.wire(
        modules=[
            dependencies,
            endpoints,
            error_handlers,
            event_handlers,
            middleware,
            test_endpoints,
        ],
        packages=[],
    )
    fastapi_settings = container.fastapi_settings()

    return pipe(
        fastapi_settings.create_fastapi(),
        # bootstrap commons
        dependencies.bootstrap,
        middleware.bootstrap,
        error_handlers.bootstrap,
        event_handlers.bootstrap,
        # bootstrap endpoints and sub routes
        endpoints.bootstrap,
        test_endpoints.bootstrap,
    )
