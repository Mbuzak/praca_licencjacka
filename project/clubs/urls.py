from django.urls import path, include

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home_club'),
    path('create/', CreateClub.as_view(), name='create_club'),
    path('<int:pk>/', DetailClub.as_view(), name='detail_club'),
    path('update/<int:pk>/', UpdateClub.as_view(), name='update_club'),
    path('delete/<int:pk>/', DeleteClub.as_view(), name='delete_club'),
    path('<int:pk>/join/', CreateClubMember.as_view(), name='join_club'),
    path('<int:pk>/leave/', DeleteClubMember.as_view(), name='leave_club'),
    path('<int:pk>/leave2/', LeaveClub.as_view(), name='leave_club2'),
]
