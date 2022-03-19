import os
from celery import Celery
from conf import settings
from typing import List, Tuple
from ml.annealing import AnnealingOptimizer

celery_app = Celery("optimizer")

celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery_app.conf.result_expires = settings.celery_result_ttl
celery_app.conf.update(task_track_started=True)


@celery_app.task(name='create_optimize_task')
def create_optimize_task(iterations: int,
                         points_payload: List[Tuple[float, float]]) -> List[Tuple[float, float, int]]:
    model = AnnealingOptimizer(iterations=iterations)
    ordered_points = model.get_route(points_payload)
    return ordered_points
