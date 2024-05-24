from rest_framework.serializers import ModelSerializer

from .models import Board, Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"