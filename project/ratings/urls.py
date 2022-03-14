from django.urls import path
from .views import *


urlpatterns = [
    path('create_fide/', CreateFideView.as_view(), name='create_fide'),
]
