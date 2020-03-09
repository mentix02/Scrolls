from parchment.views import ParchmentListView, ParchmentDetailView

from django.urls import path

app_name = 'parchment'

urlpatterns = [
    path('', ParchmentListView.as_view(), name='list'),
    path('tag/<slug:slug>/', ParchmentDetailView.as_view(), name='tag'),
    path('detail/<slug:slug>/', ParchmentDetailView.as_view(), name='detail')
]
