from django.urls import path

from .views import *

urlpatterns = [
    path("recording_data/", RecordingData.as_view()),
    path("recordings/", RecordingFiles.as_view()),
]
