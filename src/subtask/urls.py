from django.urls import path
from django.urls import register_converter
from django.urls.converters import UUIDConverter

from .views import SubtaskCreateView, SubtaskDeleteView, SubtaskDetailView, SubtaskListView, SubtaskUpdateView

register_converter(UUIDConverter, 'uuid')

app_name = "subtask"

urlpatterns = [
    path('<uuid:task_pk>/', SubtaskListView.as_view(), name='subtasks'),
    path('<uuid:task_pk>/create/', SubtaskCreateView.as_view(), name='subtask_create'),
    path('<uuid:task_pk>/detail/<uuid:pk>/', SubtaskDetailView.as_view(), name='subtask_detail'),
    path('<uuid:task_pk>/update/<uuid:pk>/', SubtaskUpdateView.as_view(), name='subtask_update'),
    path('<uuid:task_pk>/delete/<uuid:pk>/', SubtaskDeleteView.as_view(), name='subtask_delete'),
]