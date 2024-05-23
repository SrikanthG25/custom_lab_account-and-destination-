from django.urls import path
from .views import *

urlpatterns = [
    path('login/',AccoutnLoginView.as_view())

]