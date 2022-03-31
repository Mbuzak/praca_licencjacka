from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from .forms import RegisterForm
from .models import Account
from tournaments.models import TournamentMember
from ratings.models import FideHistory
from django.views.generic.list import ListView


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class IndexView(ListView):
    model = Account
    template_name = 'accounts/index.html'
    # context_object_name = 'tournaments'
    # paginate_by = 2


class ProfileView(DetailView):
    model = Account
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tournaments'] = TournamentMember.objects.filter(person=self.kwargs['pk'])
        #context['titles'] = PolishRating.objects.filter(person=self.request.user)
        context['fide_history'] = FideHistory.objects.filter(person_id=self.kwargs['pk'])

        return context


class UpdateAccountFideView(UpdateView):
    model = Account
    fields = ('fide_number',)
    template_name = 'accounts/update_fide.html'
    success_url = reverse_lazy('home_accounts')
