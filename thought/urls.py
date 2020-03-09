from django.urls import path

from thought.views import (
    ThoughtListView,
    ThoughtListAPIView,
    ThoughtDeleteAPIView,
    ThoughtCreateAPIView,
)

app_name = 'thoughts'

urlpatterns = [
    path('', ThoughtListView.as_view(), name='list'),
    path('list', ThoughtListAPIView.as_view(), name='api'),
    path('new/', ThoughtCreateAPIView.as_view(), name='create'),
    path('delete/', ThoughtDeleteAPIView.as_view(), name='delete'),
]
