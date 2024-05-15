from itertools import groupby
from django.shortcuts import render
from django.db.models import Case, When, IntegerField
from django.db.models.aggregates import Count
from django.views.decorators.csrf import csrf_exempt 

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from tasks.models import STATUSES, Board, Task
from tasks.service import send_notification


def boards(request):
    boards = Board.objects\
        .annotate(
            total=Count('task'),
            complete=Count(
                Case(
                    When(task__status='closed', then=1),
                    output_field=IntegerField()
                )
            )
        )\
        .all()
    return render(request, 'boards.html', {'boards': boards})


def tasks(request, board_id:int):
    board = Board.objects.get(pk=board_id)
    tasks = Task.objects.filter(board=board)
    statuses = STATUSES

    grouped_tasks = {k: list(v) for k, v in groupby(tasks, key=lambda t: t.status)}

    context = {
        'statuses': statuses,
        'tasks': grouped_tasks,
        'board': board
    }
    return render(request, 'tasks.html', context)


@csrf_exempt
@api_view(['PUT'])
def update_task(request, pk):
    status = request.data.get('status')
    task = Task.objects.get(pk=pk)
    task.status = status
    task.save()
    send_notification.delay(pk)
    return Response(status=HTTP_204_NO_CONTENT)
