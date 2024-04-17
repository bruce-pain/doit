from rest_framework import viewsets

from doit_api.models import Task
from doit_api.serializer import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
