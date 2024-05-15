from django.contrib import admin

from tasks.models import Board, Task

class BoardItemAdmin(admin.ModelAdmin):
    list_filter = ('status',)

@admin.register(Board)
class BoardAdmin(BoardItemAdmin):
    pass


@admin.register(Task)
class TaskAdmin(BoardItemAdmin):
    pass
