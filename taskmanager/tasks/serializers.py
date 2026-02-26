from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ['id','owner','title','description','due_date','priority','status','completed_at','created_at','updated_at']
        read_only_fields = ['completed_at','created_at','updated_at','owner']

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def update(self, instance, validated_data):
        if instance.status == 'completed':
            new_status = validated_data.get('status', instance.status)
            if new_status != 'pending':
                raise serializers.ValidationError("Completed tasks cannot be edited unless reverted to pending.")
        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id','username','email','tasks']
