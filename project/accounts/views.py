from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from accounts.forms import RegisterForm
from accounts.models import Account
from tournaments.models import TournamentMember

# Create your views here.


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register/register.html'
    success_url = reverse_lazy('login')


# UpdateView
class ProfileView(DetailView):
    model = Account
    template_name = 'register/profile.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_tournaments'] = TournamentMember.objects.all()
        return context
