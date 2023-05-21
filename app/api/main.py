from fastapi import FastAPI
from toolz import pipe

from .common import dependencies, endpoints, error_handlers, event_handlers, middleware


def bootstrap() -> FastAPI:
    """Factory function for FastAPI."""
    # Initialize dependency container
    container = dependencies.Container(
        # Abstract dependencies are configured via override or arguments for Container
        # constructor
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
    )
