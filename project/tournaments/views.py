from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Max, F, Min
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View
from .models import *
from .forms import TournamentForm
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from ratings.models import PolishRating


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
        context['tournament'] = Tournament.objects.get(pk=self.object.id)
        context['members'] = TournamentMember.objects.filter(tournament=self.object.id)
        context['is_member'] = TournamentMember.objects.all().filter(person=self.request.user.id, tournament=self.object.id)
        context['members_rating'] = PolishRating.objects.filter(tournament=self.object.id)
        context['ratings'] = PolishRating.objects.values('person').annotate(Min('name')).order_by()
        return context


class CreateTournament(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TournamentForm
    template_name = 'tournaments/create.html'
    success_url = reverse_lazy('home_tournaments')

    def get_success_message(self, cleaned_data):
        return '%(name)s został pomyślnie utworzony' % {'name': self.object.name}


class UpdateTournament(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tournament
    template_name = 'tournaments/update.html'
    fields = ('judge',)
    success_url = reverse_lazy('home_tournaments')

    def get_success_message(self, cleaned_data):
        return '%(name)s został zaktualizowany' % {'name': self.object.name}


class DeleteTournament(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Tournament
    template_name = 'tournaments/delete.html'
    success_url = reverse_lazy('home_tournaments')
    success_message = '%(name)s został pomyślnie usunięty'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': self.get_object().name})
        return super(DeleteTournament, self).delete(request, *args, **kwargs)


class CreateMember(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, application_id):
        application = TournamentApplication.objects.get(pk=application_id)
        TournamentMember(person_id=application.person.id, tournament_id=application.tournament.id).save()
        TournamentApplication(pk=application.id).delete()

        return HttpResponseRedirect('/tournaments')

    success_message = 'Pomyślnie dołączono do turnieju'

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CreateMember, self).dispatch(request, *args, **kwargs)


class DeleteMember(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TournamentMember
    # template_name = 'tournaments/leave.html'
    # fields = '__all__'
    success_url = reverse_lazy('home_tournaments')

    success_message = 'Pomyślnie opuszczono %(name)s'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': self.get_object().tournament.name})
        return super(DeleteMember, self).delete(request, *args, **kwargs)


class CreateApplication(LoginRequiredMixin, SuccessMessageMixin, View):
    # model = Tournament

    def get(self, request, pk):
        TournamentApplication(person_id=self.request.user.id, tournament_id=pk).save()

        url = reverse_lazy('detail_tournament_application', kwargs={'pk': pk})
        return HttpResponseRedirect(url)


class IndexApplication(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = 'tournaments/application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournament'] = Tournament.objects.get(pk=self.object.id)
        context['applications'] = TournamentApplication.objects.filter(tournament_id=self.object.id)
        context['has_application'] = TournamentApplication.objects.filter(person_id=self.request.user.id,
                                                                          tournament_id=self.object.id)
        context['is_member'] = TournamentMember.objects.filter(person_id=self.request.user.id,
                                                               tournament_id=self.object.id)
        return context


class DeleteApplication(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TournamentApplication
    # template_name = 'tournaments/leave.html'
    # fields = '__all__'
    success_url = reverse_lazy('home_tournaments')

    success_message = 'Pomyślnie usunięto zgłoszenie'

    #def delete(self, request, *args, **kwargs):
    #    messages.success(self.request, self.success_message % {'name': self.get_object().tournament.name})
    #    return super(DeleteTournamentMember, self).delete(request, *args, **kwargs)
