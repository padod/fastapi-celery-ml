import logging

from fastapi import FastAPI

from conf import settings
from routers import optimize, monitor

__version__ = "1.0.0"

log = logging.getLogger(__name__)

app = FastAPI(
    title="Annealing route optimizer",
    openapi_prefix=settings.api_prefix,
    version=__version__,
)

app.include_router(
    monitor.router, prefix="", responses={404: {"description": "Not found"}}
)

app.include_router(
    optimize.router,
    prefix="/optimization",
    responses={404: {"description": "Not found"}},
)


# @app.on_event("startup")
# async def startup():
#     app.state.settings = settings
#
#     try:
#         coroutine = ml.on_startup(app)
#         if asyncio.iscoroutine(coroutine):
#             await coroutine
#     except Exception as e:
#         try:
#             await shutdown()
#         finally:
#             raise e
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     try:
#         coroutine = ml.on_shutdown(app)
#         if asyncio.iscoroutine(coroutine):
#             await coroutine
#     except Exception as e:
#         raise e
