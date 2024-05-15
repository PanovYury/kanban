from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from tasks.models import Board, Task

class BoardItemAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('title', 'status',)

@admin.register(Board)
class BoardAdmin(BoardItemAdmin):
    pass


@admin.register(Task)
class TaskAdmin(BoardItemAdmin):
    list_display = ('title', 'status', 'board')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related('board')
