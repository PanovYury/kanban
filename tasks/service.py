import httpx
import logging

from celery import shared_task

LOGGER = logging.getLogger(__name__)

@shared_task
def send_notification(task: dict):
    """Send notification about update tasks status to user"""
    httpx.post('http://centrifugo/api/publish', json={
        'channel': f'tasks-{task['board']}',
        'data': task
    })