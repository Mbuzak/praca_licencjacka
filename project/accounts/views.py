from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .forms import RegisterForm
from .models import Account
from tournaments.models import TournamentMember
from ratings.models import PolishRating


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
        context['active_tournaments'] = TournamentMember.objects.filter(person=self.request.user)
        context['titles'] = PolishRating.objects.filter(person=self.request.user)
        context['best_title'] = PolishRating.objects.filter(person=self.request.user).order_by('name')[0]
        return context
