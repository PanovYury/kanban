import django_filters.rest_framework as filters

from .models import Board, Task


class TaskFilterset(filters.FilterSet):
    class Meta:
        model = Task
        fields = "__all__"


class BoardFilterset(filters.FilterSet):
    class Meta:
        model = Board
        fields = "__all__"