from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home_tournaments'),
    path('create/', CreateTournament.as_view(), name='create_tournament'),
    path('<int:pk>/', DetailTournament.as_view(), name='detail_tournament'),
    path('update/<int:pk>/', UpdateTournament.as_view(), name='update_tournament'),
    path('delete/<int:pk>/', DeleteTournament.as_view(), name='delete_tournament'),
    path('<int:application_id>/join/', CreateMember.as_view(), name='create_tournament_member'),
    path('<int:pk>/join-all/', AddMembersView.as_view(), name='create_tournament_members'),
    path('<int:pk>/leave/', DeleteMember.as_view(), name='leave_tournament'),
    path('<int:pk>/application/create', CreateApplication.as_view(), name='create_tournament_application'),
    path('<int:pk>/application/', IndexApplication.as_view(), name='detail_tournament_application'),
    path('<int:pk>/application/delete/', DeleteApplication.as_view(), name='delete_tournament_application'),
    # rounds
    path('<int:tournament_id>/round/<int:pk>/', RoundView.as_view(), name='detail_round'),
    path('<int:pk>/round/create/', CreateRound.as_view(), name='create_round'),
    # matches
    path('<int:tournament_id>/round/<int:round_id>/result/<int:pk>/', UpdateMatch.as_view(), name='tournaments_update_match'),
    # members
    path('<int:pk>/members', MembersView.as_view(), name='tournament_members'),
    path('<int:pk>/members/<int:member_id>', ProfileView.as_view(), name='tournament_profile'),
    path('<int:pk>/placement/', PlacementView.as_view(), name='tournaments_placement'),
    # statistics
    path('<int:pk>/stats/', StatisticsView.as_view(), name='tournaments_statistics'),
    # update tournament
    path('<int:pk>/start-tournament/', StartTournamentView.as_view(), name='tournaments_begin_tournament'),
    path('<int:pk>/end-tournament', EndTournamentView.as_view(), name='tournaments_end_tournament'),
]
