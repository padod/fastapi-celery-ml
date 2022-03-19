import logging
from typing import List, Tuple

from celery.result import AsyncResult
from fastapi import APIRouter
from starlette.responses import JSONResponse

from datamodels.annealing import OptimizerResponse, Payload, Point, WorkerPostResponse, WorkerGetResponse, Points
from conf import MLSettings
from celery_app import create_optimize_task

log = logging.getLogger(__name__)

router = APIRouter()

config = MLSettings()


@router.post("/optimize", response_model=WorkerPostResponse)
async def optimize(payload: Points) -> WorkerPostResponse:
    task = create_optimize_task.delay(
        iterations=config.max_iterations,
        points_payload=payload.unpack(payload))
    return WorkerPostResponse(id=task.id, status=task.status)


@router.get("/optimized/{task_id}")
async def optimized(task_id: str):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    log.warning(result)
    return result
