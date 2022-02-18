from django.urls import path, include

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('create/', CreateTournament.as_view(), name='create_tournament'),
    path('<int:pk>/', DetailTournament.as_view(), name='detail_tournament'),
    path('update/<int:pk>/', UpdateTournament.as_view(), name='update_tournament'),
    path('delete/<int:pk>/', DeleteTournament.as_view(), name='delete_tournament'),
    path('join/', CreateTournamentMember.as_view(), name='join_tournament'),
]
