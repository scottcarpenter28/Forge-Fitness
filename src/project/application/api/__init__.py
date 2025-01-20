from django.urls import path

from .api_routine import RoutineAPIView


api_urls = [
    path("routine/<str:routine_id>", RoutineAPIView.as_view(), name="api-routine"),
    path("routine/", RoutineAPIView.as_view(), name="api-routine"),
]
