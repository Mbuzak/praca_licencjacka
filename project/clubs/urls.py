from django.urls import path, include

from .views import *

urlpatterns = [
    # club
    path('', IndexView.as_view(), name='home_club'),
    path('create/', CreateClub.as_view(), name='create_club'),
    path('<int:pk>/', DetailClub.as_view(), name='detail_club'),
    path('update/<int:pk>/', UpdateClub.as_view(), name='update_club'),
    path('delete/<int:pk>/', DeleteClub.as_view(), name='delete_club'),
    path('<int:pk>/leave/', DeleteClubMember.as_view(), name='leave_club'),
    path('<int:pk>/leave2/', LeaveClub.as_view(), name='leave_club2'),
    # member
    path('<int:application_id>/join/', CreateMember.as_view(), name='create_club_member'),
    # application
    path('<int:pk>/application/', IndexApplication.as_view(), name='detail_club_application'),
    path('<int:pk>/application/create', CreateApplication.as_view(), name='create_club_application'),
    path('<int:pk>/application/delete/', DeleteApplication.as_view(), name='delete_club_application'),
]
