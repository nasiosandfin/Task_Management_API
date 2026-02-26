from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status','priority','due_date']
    ordering_fields = ['due_date','priority']
    search_fields = ['title','description']

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='toggle-complete')
    def toggle_complete(self, request, pk=None):
        task = self.get_object()
        if task.status == 'pending':
            task.mark_complete()
            return Response({'status':'completed','completed_at':task.completed_at}, status=status.HTTP_200_OK)
        else:
            task.mark_incomplete()
            return Response({'status':'pending'}, status=status.HTTP_200_OK)


