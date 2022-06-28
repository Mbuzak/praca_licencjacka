from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name='home_accounts'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('promotion/<int:pk>/', UpdateCategory.as_view(), name='accounts_update_category'),
    path('decline-promotion/<int:pk>/', DeclineCategory.as_view(), name='accounts_decline_category'),
]
