from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, DetailView
from .models import *
from .forms import TournamentForm
from django.urls import reverse_lazy
from extra_views import CreateWithInlinesView, InlineFormSetView
from django.views.generic.list import ListView


class IndexView(ListView):
    template_name = 'tournaments/index.html'
    queryset = Tournament.objects.all()
    # context_object_name = 'tournaments'
    # paginate_by = 30


class DetailTournament(DetailView):
    model = Tournament
    template_name = 'tournaments/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournament'] = Tournament.objects.get()
        context['members'] = TournamentMember.objects.all()
        return context


# CRUD

# CreateWithInlinesView instead of CreateView
class CreateTournament(LoginRequiredMixin, CreateView):
    form_class = TournamentForm
    template_name = 'tournaments/create.html'
    success_url = reverse_lazy('home')


class UpdateTournament(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tournament
    template_name = 'tournaments/update.html'
    fields = ('id_judge',)
    success_url = reverse_lazy('home')

    def get_success_message(self, cleaned_data):
        return '%(name)s został zaktualizowany' % {'name': self.object.name}


class DeleteTournament(LoginRequiredMixin, DeleteView):
    model = Tournament
    template_name = 'tournaments/delete.html'
    success_url = reverse_lazy('home')


class CreateTournamentMember(LoginRequiredMixin, CreateView):
    model = TournamentMember
    template_name = 'tournaments/join.html'
    fields = '__all__'
    success_url = reverse_lazy('home')
