from django.urls import path, include
from .views import SummarizerView

urlpatterns = [
    path('summarize/<str:audio_id>/',
         SummarizerView.as_view(), name='summarize'),


]
