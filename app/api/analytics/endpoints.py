"""Module for storing request/response handlers.

As an agreement handler functions are called as: <method>_<route>
For example if handler has full route: GET task/{uid} function is called get_task_uid
They can ignore docstrings, but description is required.
"""
import aiohttp
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, FastAPI, Path, Query, status
from fastapi.responses import JSONResponse, Response

from app.api.common.dependencies import Container
from app.core.commit.vault import AbstractCommitVault

router = APIRouter(prefix="/task", tags=["Task"])


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize task router for app."""
    app.include_router(router)
    return app


@router.get(
    "/",
    description="Create new task from base information",
    response_description="Successfully create new task",
    status_code=201,
)
@inject
async def post_task(
    repo: AbstractCommitVault = Depends(Provide[Container.commit_repository]),
):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url="https://api.github.com/repos/spbu-registry/Backend-registry/commits",
            headers={
                "Authorization": "Bearer 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"
            },
        ) as response:
            if response.status != 200:
                print(await response.status)

    print(await repo.read_all())
