from django.urls import path
from .views import SearchView


app_name = "core"

urlpatterns = [
    path('search/', SearchView.as_view(), name='global_search'),
]