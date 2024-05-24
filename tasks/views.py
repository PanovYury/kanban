import logging
from django.shortcuts import render
from django.db.models import Case, When, IntegerField
from django.db.models.aggregates import Count

from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from django_filters import rest_framework as filters

from tasks.filters import TaskFilterset
from tasks.models import STATUSES, Board, Task
from tasks.serializers import TaskSerializer
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
    statuses = STATUSES

    context = {
        'statuses': statuses,
        'board': board
    }
    return render(request, 'tasks.html', context)


class TasksViewSet(GenericViewSet, ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    filterset_class = TaskFilterset
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = Task.objects.all()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        send_notification.delay(serializer.data)
