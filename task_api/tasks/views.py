from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth.models import User

# Task ViewSet
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return tasks owned by the logged-in user
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the owner to the logged-in user
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'Completed'
        task.completed_at = timezone.now()
        task.save()
        return Response({'status': 'Task marked as complete'})

    @action(detail=True, methods=['post'])
    def incomplete(self, request, pk=None):
        task = self.get_object()
        task.status = 'Pending'
        task.completed_at = None
        task.save()
        return Response({'status': 'Task reverted to incomplete'})


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow registration without login






from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return tasks belonging to the logged-in user
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the owner when creating a task
        serializer.save(owner=self.request.user)

# Create your views here.
