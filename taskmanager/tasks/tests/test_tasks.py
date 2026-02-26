import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task

@pytest.mark.django_db
def test_create_task_future_due_date():
    user = User.objects.create_user('u','u@example.com','pass')
    client = APIClient()
    client.force_authenticate(user=user)
    due = (timezone.now() + timedelta(days=2)).isoformat()
    resp = client.post('/api/tasks/', {'title':'T','due_date':due,'priority':'low'})
    assert resp.status_code == 201
    assert resp.data['title'] == 'T'
    assert resp.data['priority'] == 'low'

@pytest.mark.django_db
def test_create_task_past_due_date_fails():
    user = User.objects.create_user('u','u@example.com','pass')
    client = APIClient()
    client.force_authenticate(user=user)
    due = (timezone.now() - timedelta(days=1)).isoformat()
    resp = client.post('/api/tasks/', {'title':'T','due_date':due,'priority':'low'})
    assert resp.status_code == 400
    assert 'due_date' in resp.data

@pytest.mark.django_db
def test_task_ownership_enforced():
    user1 = User.objects.create_user('u1','u1@example.com','pass')
    user2 = User.objects.create_user('u2','u2@example.com','pass')
    task = Task.objects.create(owner=user1, title='Owned', due_date=timezone.now()+timedelta(days=1))
    client = APIClient()
    client.force_authenticate(user=user2)
    resp = client.get(f'/api/tasks/{task.id}/')
    # user2 should not see user1's task
    assert resp.status_code == 404

@pytest.mark.django_db
def test_completed_task_cannot_be_edited():
    user = User.objects.create_user('u','u@example.com','pass')
    client = APIClient()
    client.force_authenticate(user=user)
    task = Task.objects.create(owner=user, title='Done', due_date=timezone.now()+timedelta(days=1), status='completed', completed_at=timezone.now())
    resp = client.put(f'/api/tasks/{task.id}/', {'title':'Edited','due_date':(timezone.now()+timedelta(days=2)).isoformat(),'priority':'high'})
    assert resp.status_code == 400
    assert 'Completed tasks cannot be edited' in str(resp.data)

@pytest.mark.django_db
def test_mark_task_complete_and_incomplete():
    user = User.objects.create_user('u','u@example.com','pass')
    client = APIClient()
    client.force_authenticate(user=user)
    task = Task.objects.create(owner=user, title='MarkMe', due_date=timezone.now()+timedelta(days=1))
    # Mark complete
    resp = client.post(f'/api/tasks/{task.id}/mark/', {'status':'completed'})
    assert resp.status_code == 200
    assert resp.data['status'] == 'completed'
    assert resp.data['completed_at'] is not None
    # Mark back to pending
    resp = client.post(f'/api/tasks/{task.id}/mark/', {'status':'pending'})
    assert resp.status_code == 200
    assert resp.data['status'] == 'pending'
    assert resp.data['completed_at'] is None

@pytest.mark.django_db
def test_filter_and_sort_tasks():
    user = User.objects.create_user('u','u@example.com','pass')
    client = APIClient()
    client.force_authenticate(user=user)
    Task.objects.create(owner=user, title='Low', due_date=timezone.now()+timedelta(days=2), priority='low')
    Task.objects.create(owner=user, title='High', due_date=timezone.now()+timedelta(days=1), priority='high')
    # Filter by priority
    resp = client.get('/api/tasks/?priority=high')
    assert resp.status_code == 200
    assert all(t['priority']=='high' for t in resp.data)
    # Sort by due_date ascending
    resp = client.get('/api/tasks/?ordering=due_date')
    assert resp.status_code == 200
    due_dates = [t['due_date'] for t in resp.data]
    assert due_dates == sorted(due_dates)
