from django.db.models import Max, Min
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from .forms import RegisterForm
from .models import Account
from tournaments.models import TournamentMember
from ratings.models import PolishRating
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
        context['active_tournaments'] = TournamentMember.objects.filter(person=self.request.user)
        context['titles'] = PolishRating.objects.filter(person=self.request.user)
        # context['best_title'] = PolishRating.objects.filter(person=self.request.user).order_by('name')
        context['best_title'] = PolishRating.objects.filter(person=self.request.user).aggregate(Min('name'))
        # context['best_title'] = PolishRating.objects.filter(person=self.request.user).values('name').annotate(Max('name')).distinct()
        # context['best_title'] = PolishRating.objects.filter(person=self.request.user).values('name').annotate(Max('obtain'))
        return context
