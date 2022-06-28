from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View
from accounts.models import Account
from .models import *
from .forms import TournamentForm
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from ratings.models import FideRating
from .calculate import (create_pairing, create_round,
                        get_fide_rating,
                        update_results,
                        round_count,
                        set_participants_promotion,
                        is_match_result_valid,
                        )
from joinment.models import Application
from .pairing import Swiss
from .filters import TournamentFilter


def tournament_round_count(tournament_id):
    rounds = Round.objects.filter(tournament_id=tournament_id)
    if rounds:
        return rounds.latest('round').round
    return 0


def swiss_pairing(tournament_id):
    players = []
    games = []

    members = TournamentMember.objects.filter(tournament_id=tournament_id)
    matches = Match.objects.filter(round__tournament_id=tournament_id)

    for member in members:
        # player - [member_id, polish_rating, current_score, does_already_have_break]
        players.append([member.id, member.person.get_rating(), member.points])

    for i in range(1, tournament_round_count(tournament_id)):
        round_matches = matches.filter(round__round=i)

        for match in round_matches:
            white = TournamentMember.objects.get(tournament_id=match.round.tournament.id, person_id=match.white.person.id)
            black = TournamentMember.objects.get(tournament_id=match.round.tournament.id, person_id=match.black.person.id)

            games.append({'white': white.id, 'black': black.id, 'white_score': white.points,
                          'black_score': black.points, 'round': i})

    swiss = Swiss(players, games, tournament_round_count(tournament_id))
    swiss.pairing()

    for i in range(len(swiss.pairs)):
        Match(round_id=Round.objects.filter(tournament_id=tournament_id).latest('round').id, chessboard=i + 1,
              white_id=swiss.pairs[i][0], black_id=swiss.pairs[i][1]).save()


class IndexView(ListView):
    template_name = 'tournaments/index.html'
    queryset = Tournament.objects.all().order_by('start')
    # context_object_name = 'tournaments'
    # paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TournamentFilter(self.request.GET, queryset=self.get_queryset())
        return context


class DetailTournament(DetailView):
    model = Tournament
    template_name = 'tournaments/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_member'] = TournamentMember.objects.filter(person=self.request.user.id, tournament=self.object.id)
        context['members'] = TournamentMember.objects.filter(tournament_id=self.object.id)
        context['rounds'] = Round.objects.filter(tournament_id=self.object.id).values('id', 'round')
        context['round_count'] = round_count(self.object.id)
        context['last_round'] = False
        if context['rounds']:
            context['last_round'] = Round.objects.filter(tournament_id=self.object.id).latest('round')

        matches = Match.objects.filter(round__tournament__id=self.object.id)
        context['incompleted_matches'] = len([[x.white_result, x.black_result] for x in matches
                                              if x.white_result is None or x.black_result is None])

        """
        for i in Account.objects.all():
            if 'gmail.com' in i.email:
                TournamentMember(tournament_id=37, person_id=i.id, title=Account.objects.get(pk=i.id).title).save() # fide rating
        """

        return context


class MembersView(DetailView):
    model = Tournament
    template_name = 'tournaments/members.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = sorted(TournamentMember.objects.filter(tournament=self.object.id),
                                    key=lambda x: (get_fide_rating(x.person.id, self.object.game_type),
                                                   x.person.get_rating()), reverse=True)
        members_id = [item.person.id for item in context['members']]
        context['fide'] = FideRating.objects.filter(person_id__in=members_id)
        return context


class ProfileView(DetailView):
    model = Tournament
    template_name = 'tournaments/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member'] = TournamentMember.objects.get(pk=self.kwargs['member_id'])
        rounds = [item.id for item in Round.objects.filter(tournament_id=self.kwargs['pk'])]
        context['matches'] = Match.objects.filter(Q(white_id=self.kwargs['member_id']) |
                                                  Q(black_id=self.kwargs['member_id']), round_id__in=rounds)
        return context


class CreateTournament(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    form_class = TournamentForm
    template_name = 'tournaments/create.html'
    success_url = reverse_lazy('home_tournaments')
    permission_required = ('add_tournament',)

    def get_success_message(self, cleaned_data):
        return '%(name)s został pomyślnie utworzony' % {'name': self.object.name}

    def form_valid(self, form):
        form.instance.judge = Account.objects.get(pk=self.request.user.id)
        return super(CreateTournament, self).form_valid(form)


class UpdateTournament(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tournament
    fields = ('name', 'start', 'end', 'place', 'round_number', 'description')
    template_name = 'tournaments/update.html'

    def get_success_url(self):
        return reverse_lazy('detail_tournament', kwargs={'pk': self.kwargs['pk']})

    def get_success_message(self, cleaned_data):
        return '%(name)s został zaktualizowany' % {'name': self.object.name}


class DeleteTournament(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Tournament
    success_url = reverse_lazy('home_tournaments')
    success_message = '%(name)s został pomyślnie usunięty'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': self.get_object().name})
        return super(DeleteTournament, self).delete(request, *args, **kwargs)


class CreateMember(LoginRequiredMixin, View):
    def post(self, request, application_id):
        application = Application.objects.get(pk=application_id)
        person = application.person

        if FideRating.objects.filter(person_id=person.id):
            TournamentMember(person_id=person.id, tournament_id=application.tournament.id, title=person.title,
                             fide_rating=get_fide_rating(person.id, application.tournament.game_type)).save()
        else:
            TournamentMember(person_id=person.id, tournament_id=application.tournament.id, title=person.title).save()

        Application(pk=application.id).delete()

        url = reverse_lazy('detail_tournament_application', kwargs={'pk': application.tournament.id})
        return HttpResponseRedirect(url)


class AddMembersView(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, pk):
        applications = Application.objects.filter(tournament_id=pk)

        for application in applications:
            person = application.person
            if FideRating.objects.filter(person_id=person.id):
                TournamentMember(person_id=person.id, tournament_id=application.tournament.id, title=person.title,
                                 fide_rating=get_fide_rating(person.id, application.tournament.game_type)).save()
            else:
                TournamentMember(person_id=person.id, tournament_id=application.tournament.id,
                                 title=person.title).save()

            TournamentMember(person_id=application.person.id, tournament_id=pk).save()
            Application(pk=application.id).delete()

        url = reverse_lazy('detail_tournament_application', kwargs={'pk': pk})
        return HttpResponseRedirect(url)

    success_message = 'Pomyślnie dodano wszystkich do turnieju'

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AddMembersView, self).dispatch(request, *args, **kwargs)


class DeleteMember(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TournamentMember
    template_name = 'tournaments/delete_member.html'
    success_url = reverse_lazy('home_tournaments')
    success_message = 'Pomyślnie opuszczono %(name)s'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': self.get_object().tournament.name})
        return super(DeleteMember, self).delete(request, *args, **kwargs)


class RoundView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Round
    template_name = 'tournaments/round.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['matches'] = Match.objects.filter(round__tournament__id=self.kwargs['tournament_id'], round=self.kwargs['pk'])
        context['rounds'] = Round.objects.filter(tournament_id=self.kwargs['tournament_id']).values('id', 'round')
        context['round_number'] = Round.objects.get(id=self.kwargs['pk']).round
        context['tournament'] = Tournament.objects.get(id=self.kwargs['tournament_id'])
        return context


class CreateRound(LoginRequiredMixin, View):
    # pk - tournament_id
    def post(self, request, pk):
        game_system = Tournament.objects.get(pk=pk).game_system

        update_results(pk)
        create_round(pk)

        if game_system == 'szwajcarski':
            swiss_pairing(pk)
        elif game_system == 'kołowy(rundowy)':
            create_pairing(pk)
        else:
            print('Provided game system not found')

        url = reverse_lazy('detail_tournament', kwargs={'pk': pk})
        return HttpResponseRedirect(url)


class UpdateMatch(LoginRequiredMixin, UpdateView):
    model = Match
    template_name = 'tournaments/match_result.html'
    fields = ('white_result', 'black_result')
    success_url = reverse_lazy('home_tournaments')

    def get_success_url(self):
        return reverse_lazy('detail_round',
                            kwargs={'tournament_id': self.kwargs['tournament_id'], 'pk': self.kwargs['round_id']})

    def form_valid(self, form):
        if is_match_result_valid(form.instance.white_result, form.instance.black_result):
            return super(UpdateMatch, self).form_valid(form)
        return super(UpdateMatch, self).form_invalid(form)


class PlacementView(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = 'tournaments/placement.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = sorted(TournamentMember.objects.filter(tournament=self.object.id),
                                    key=lambda x: (x.points, get_fide_rating(x.person.id, self.object.game_type),
                                                   x.person.get_rating()), reverse=True)
        members_id = [item.person.id for item in context['members']]
        context['fide'] = FideRating.objects.filter(person_id__in=members_id)
        return context


class StatisticsView(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = 'tournaments/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = TournamentMember.objects.filter(tournament_id=self.kwargs['pk'])
        return context


class StartTournamentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        game_system = Tournament.objects.get(pk=pk).game_system

        tournament = Tournament.objects.get(pk=pk)
        tournament.is_started = True
        tournament.save()

        # create first round
        Round(tournament_id=pk, round=1).save()

        if game_system == 'szwajcarski':
            swiss_pairing(pk)
        elif game_system == 'kołowy(rundowy)':
            create_pairing(pk)
        else:
            print('Provided game system not found')

        # delete rest of applications
        Application.objects.filter(type_of_object='T', tournament_id=pk).delete()

        url = reverse_lazy('detail_tournament', kwargs={'pk': pk})
        return HttpResponseRedirect(url)


class EndTournamentView(LoginRequiredMixin, View):
    def get(self, request, pk):
        tournament = Tournament.objects.get(pk=self.kwargs['pk'])
        tournament.is_ended = True
        tournament.save()

        update_results(pk)

        if tournament.is_polish_rated:
            set_participants_promotion(tournament)

        url = reverse_lazy('detail_tournament', kwargs={'pk': pk})
        return HttpResponseRedirect(url)


class CreateApplication(LoginRequiredMixin, SuccessMessageMixin, View):
    def post(self, request, pk):
        Application(person_id=self.request.user.id, tournament_id=pk, type_of_object='T').save()

        url = reverse_lazy('detail_tournament_application', kwargs={'pk': pk})
        return HttpResponseRedirect(url)


class IndexApplication(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = 'tournaments/application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(tournament_id=self.object.id)
        context['has_application'] = Application.objects.filter(person_id=self.request.user.id, tournament_id=self.object.id)
        context['is_member'] = TournamentMember.objects.filter(person_id=self.request.user.id, tournament_id=self.object.id)
        return context


class DeleteApplication(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Application

    def get_success_url(self):
        return reverse_lazy('detail_tournament_application', kwargs={'pk': self.object.tournament.id})

