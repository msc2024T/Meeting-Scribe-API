from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioFileViewSet

router = DefaultRouter()
router.register(r'audio-files', AudioFileViewSet, basename='audio-files')

urlpatterns = [
    path('', include(router.urls)),
]
