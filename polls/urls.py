from django.urls import path
from .views import poll_view

urlpatterns = [
    path('', poll_view, name='poll_view'),
]
