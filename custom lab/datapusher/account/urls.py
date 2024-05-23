from django.urls import path
from .views import *

urlpatterns = [
    path('incoming_data/',Accountupdation.as_view()),
    path('incoming_views/',Destinationview.as_view()),
]