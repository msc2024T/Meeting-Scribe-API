from django.urls import path, include
from .views import TranscriptionView


urlpatterns = [
    path('transcriptions/<str:audio_file_id>/', TranscriptionView.as_view(), name='create-transcription')]
