from django.db import models

STATUSES = [
    ('proposed', 'Запланирована'),
    ('active', 'Активная'),
    ('resolved', 'На проверке'),
    ('closed', 'Закрытая'),
]

class BoardItem(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    status = models.CharField(max_length=8, choices=STATUSES, blank=False, default=STATUSES[0][0])

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title

class Board(BoardItem):
    pass


class Task(BoardItem):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=False, blank=False)
