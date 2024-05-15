import logging

from celery import shared_task
import httpx

from tasks.models import Task

LOGGER = logging.getLogger(__name__)

@shared_task
def send_notification(task_id: int):
    """Send notification about update tasks status to user"""
    task = Task.objects.get(pk=task_id)
    httpx.post('http://centrifugo/api/publish', json={
        'channel': f'tasks-{task.board_id}',
        'data': {
            'task': task.title,
            'status': task.status
        }
    })