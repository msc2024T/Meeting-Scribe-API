
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('files/', include('files.urls')),
    path('transcriptions/', include('transcription.urls')),
    path('summarizer/', include('summarizer.urls')),
]
