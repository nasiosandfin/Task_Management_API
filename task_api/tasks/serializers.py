from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task
from datetime import date

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'completed_at', 'owner']
        read_only_fields = ['owner', 'completed_at']

    # Custom validation for due_date
    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    # Custom validation for status
    def validate_status(self, value):
        if value not in ['Pending', 'Completed']:
            raise serializers.ValidationError("Status must be either Pending or Completed.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date',
            'priority', 'status', 'completed_at', 'owner'
        ]
        read_only_fields = ['owner', 'completed_at']
