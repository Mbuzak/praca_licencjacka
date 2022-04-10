from django.urls import path
from .views import *

urlpatterns = [
    # club
    path('', IndexView.as_view(), name='home_club'),
    path('create/', CreateClub.as_view(), name='create_club'),
    path('<int:pk>/', DetailClub.as_view(), name='detail_club'),
    path('update/<int:pk>/', UpdateClub.as_view(), name='update_club'),
    path('delete/<int:pk>/', DeleteClub.as_view(), name='delete_club'),
    # member
    path('<int:pk>/add-member/', AddMemberView.as_view(), name='clubs_add_member'),
    path('<int:club_id>/member-leave/<int:pk>', LeaveClubView.as_view(), name='clubs_member_leave'),
    # application
    path('<int:pk>/application/', ApplicationView.as_view(), name='detail_club_application'),
    path('<int:pk>/application/create', CreateApplication.as_view(), name='create_club_application'),
    path('<int:pk>/application/delete/', DeleteApplication.as_view(), name='delete_club_application'),

]
