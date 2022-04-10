from django.contrib.auth.models import Permission, Group
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from .forms import RegisterForm
from .models import Account
from tournaments.models import TournamentMember
from ratings.models import FideHistory, FidePeriod
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class IndexView(ListView):
    model = Account
    template_name = 'accounts/index.html'
    # context_object_name = 'tournaments'
    # paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['latest_period'] = True
        latest_period = FidePeriod.objects.latest('year', 'month')
        if latest_period.month == datetime.now().month and latest_period.year == datetime.now().year:
            context['latest_period'] = False

        return context


class ProfileView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tournaments'] = TournamentMember.objects.filter(person=self.kwargs['pk'])
        context['fide_history'] = FideHistory.objects.filter(person_id=self.kwargs['pk'])

        u = Account.objects.get(pk=431)
        u2 = Account.objects.get(pk=16)
        g = Group.objects.get(name='Judge')
        p = Permission.objects.get(name='Can add tournament')

        print(p)
        print(u.get_user_permissions())
        print(u.has_perm('tournaments.add_tournament'), u2.has_perm('tournaments.add_tournament'))
        print(u.has_perm('tournaments.create_tournament'), u2.has_perm('tournaments.create_tournament'))
        print(u.has_perm(p), u2.has_perm(p))
        return context
