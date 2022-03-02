from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Max, F, Min
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from ratings.models import PolishRating


class IndexView(ListView):
    template_name = 'tournaments/index.html'
    queryset = Tournament.objects.all().order_by('start')
    # context_object_name = 'tournaments'
    # paginate_by = 30


class DetailTournament(DetailView):
    model = Tournament
    template_name = 'tournaments/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournament'] = Tournament.objects.get(pk=self.object.id)
        #context['members'] = TournamentMember.objects.filter(tournament=self.object.id)
        context['is_member'] = TournamentMember.objects.all().filter(person=self.request.user.id, tournament=self.object.id)
        # context['members_rating'] = PolishRating.objects.filter(tournament=self.object.id)
        context['rounds'] = Round.objects.filter(tournament_id=self.object.id).values('id', 'round')
        #context['ratings'] = PolishRating.objects.values('person').annotate(Min('name')).order_by()
        return context


class MembersView(DetailView):
    model = Tournament
    template_name = 'tournaments/members.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = TournamentMember.objects.filter(tournament=self.object.id)
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
    template_name = 'tournaments/delete_member.html'
    success_url = reverse_lazy('home_tournaments')
    success_message = 'Pomyślnie opuszczono %(name)s'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': self.get_object().tournament.name})
        return super(DeleteMember, self).delete(request, *args, **kwargs)


class CreateApplication(LoginRequiredMixin, SuccessMessageMixin, View):
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
    # success_message = 'Pomyślnie usunięto zgłoszenie'

    #def delete(self, request, *args, **kwargs):
    #    messages.success(self.request, self.success_message % {'name': self.get_object().tournament.name})
    #    return super(DeleteTournamentMember, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detail_tournament_application', kwargs={'pk': self.object.tournament.id})


# Matches
class RoundView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Round
    template_name = 'tournaments/round.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['matches'] = Match.objects.filter(round__tournament__id=self.kwargs['tournament_id'],
                                                  round=self.kwargs['pk'])
        context['round_number'] = Round.objects.get(id=self.kwargs['pk']).round
        return context

    """
    def post(self, request, **kwargs):
        form = MatchForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data['white_result'])
            match = Match.objects.get(id=self.kwargs['round_id'])
            match.white_result = form.cleaned_data['white_result']
            match.black_result = form.cleaned_data['black_result']
            match.save()
        else:
            print('WARNING!\n\n\n')
        # url = reverse_lazy('detail_tournament', kwargs={'pk': pk})
        # return HttpResponseRedirect(url)
        return HttpResponseRedirect('/tournaments/18/round/1/7') # TDB
    """


class CreateRound(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, pk):
        def set_round():
            if Round.objects.filter(tournament_id=pk):
                return Round.objects.filter(tournament_id=pk).aggregate(Max('round'))['round__max'] + 1
            return 1

        Round(tournament_id=pk, round=set_round()).save()

        """ There will be generate matches logic
        players = TournamentMember.objects.filter(tournament_id=pk)
        Match(tournament_id=kwargs['pk'], white=players[0].person, black=players[1].person, round=set_round(),
              chessboard=1).save()
        """

        url = reverse_lazy('detail_tournament', kwargs={'pk': pk})
        return HttpResponseRedirect(url)


class UpdateMatch(LoginRequiredMixin, UpdateView):
    model = Match
    template_name = 'tournaments/match_result.html'
    fields = ('white_result', 'black_result')
    success_url = reverse_lazy('home_tournaments')
