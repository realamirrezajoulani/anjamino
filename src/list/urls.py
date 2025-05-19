from django.urls import path
from django.urls import register_converter
from django.urls.converters import UUIDConverter

from .views import ListCreateView, ListDeleteView, ListDetailView, ListListView, ListUpdateView


register_converter(UUIDConverter, 'uuid')

app_name = "list"

urlpatterns = [
    path('', ListListView.as_view(), name='lists'),
    path('<uuid:pk>/', ListDetailView.as_view(), name='list_detail'),
    path('create/', ListCreateView.as_view(), name='list_create'),
    path('update/<uuid:pk>/', ListUpdateView.as_view(), name='list_update'),
    path('delete/<uuid:pk>/', ListDeleteView.as_view(), name='list_delete'),
]