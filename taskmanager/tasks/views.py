from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer, UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view and manage their own tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # Add filtering, ordering, and pagination support
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'priority']   # adjust to your Task model fields
    ordering_fields = ['created_at', 'due_date']  # adjust to your Task model fields
    ordering = ['-created_at']  # default ordering

    def get_queryset(self):
        # Only return tasks owned by the logged-in user
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the task owner
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admins to manage users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
