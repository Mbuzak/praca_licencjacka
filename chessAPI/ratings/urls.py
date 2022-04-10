from django.urls import path
from .views import *


urlpatterns = [
    path('update_fide_period/', UpdateFidePeriodView.as_view(), name='ratings_update_fide_period'),
    path('<int:pk>/create_fide/', CreateFideView.as_view(), name='ratings_create_fide'),
]
