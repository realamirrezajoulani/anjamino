from django.urls import path
from django.urls import register_converter
from django.urls.converters import UUIDConverter

from .views import TaskListView, TaskUpdateView, TaskDetailView, TaskCreateView, TaskDeleteView


register_converter(UUIDConverter, 'uuid')

app_name = "task"

urlpatterns = [
    path('<uuid:list_pk>/', TaskListView.as_view(), name='tasks'),
    path('<uuid:list_pk>/create/', TaskCreateView.as_view(), name='task_create'),
    path('<uuid:list_pk>/detail/<uuid:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<uuid:list_pk>/update/<uuid:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('<uuid:list_pk>/delete/<uuid:pk>/', TaskDeleteView.as_view(), name='task_delete'),
]