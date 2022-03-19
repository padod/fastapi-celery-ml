import json

from unittest.mock import patch, call

from worker.celery_worker import create_optimize_task


def test_task():
    assert True


@patch("worker.create_task.run")
def test_mock_task(mock_run):
    assert True


def test_task_status(test_app):
    assert True