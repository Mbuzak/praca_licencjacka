import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from chessAPI import settings
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View
from accounts.models import Account


class IndexView(ListView):
    template_name = 'clubs/index.html'
    queryset = Club.objects.all()
    # context_object_name = 'tournaments'
    # paginate_by = 30


class DetailClub(DetailView):
    model = Club
    template_name = 'clubs/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = Club.objects.get(id=self.object.id)
        context['members'] = ClubMember.objects.all()  # id_club, not all
        context['is_member'] = ClubMember.objects.all().filter(person=self.request.user.id, club=self.object.id)  # test it!!!!!
        return context


class CreateClub(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Club
    fields = ('name', 'email', 'address', 'manager')
    # form_class = TournamentForm
    template_name = 'clubs/create.html'
    success_url = reverse_lazy('home_club')

    def get_success_message(self, cleaned_data):
        return '%(name)s został pomyślnie utworzony' % {'name': self.object.name}


class UpdateClub(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Club
    template_name = 'clubs/update.html'
    fields = ('name', 'email', 'manager',)
    success_url = reverse_lazy('home_club')

    def get_success_message(self, cleaned_data):
        return '%(name)s został zaktualizowany' % {'name': self.object.name}


class DeleteClub(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Club
    template_name = 'clubs/delete.html'
    success_url = reverse_lazy('home_club')
    success_message = '%(name)s został pomyślnie usunięty'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': self.get_object().name})
        return super(DeleteClub, self).delete(request, *args, **kwargs)


# Members
class CreateMember(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, application_id):
        application = ClubApplication.objects.get(pk=application_id)
        ClubMember(person_id=application.person.id, club_id=application.club.id).save()
        ClubApplication(pk=application.id).delete()

        account = Account.objects.get(id=application.person.id)
        account.club = Club.objects.get(id=application.club.id)
        account.save()

        return HttpResponseRedirect('/clubs')

    success_message = 'Pomyślnie dołączono do klubu'

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CreateMember, self).dispatch(request, *args, **kwargs)


# WARNING: not used model
class DeleteClubMember(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClubMember
    # template_name = 'tournaments/leave.html'
    # fields = '__all__'
    success_url = reverse_lazy('home_club')

    success_message = 'Pomyślnie opuszczono klub %(name)s'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': self.get_object().club.name})
        return super(DeleteClubMember, self).delete(request, *args, **kwargs)


class LeaveClub(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ClubMember
    template_name = 'clubs/update.html'
    fields = ()
    # initial = {'value1': 'foo', 'value2': 'bar'}
    # fields = ('person',)
    # fields = ('name', 'email', 'manager',)
    success_url = reverse_lazy('home_club')

    def get_success_message(self, cleaned_data):
        return 'Klub %(name)s został opuszczony' % {'name': self.object.club.name}

    #def post(self, request, **kwargs):
    #    request.POST = request.POST.copy()
    #    request.POST['leave'] = datetime.date.today()
    #    return super(LeaveClub, self).post(request, **kwargs)


# Applications
class IndexApplication(LoginRequiredMixin, DetailView):
    model = Club
    template_name = 'clubs/application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = Club.objects.get(pk=self.object.id)
        context['applications'] = ClubApplication.objects.filter(club_id=self.object.id)
        context['has_application'] = ClubApplication.objects.filter(person_id=self.request.user.id,
                                                                    club_id=self.object.id)
        context['is_member'] = ClubMember.objects.filter(person_id=self.request.user.id)
        return context


class CreateApplication(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, pk):
        ClubApplication(person_id=self.request.user.id, club_id=pk).save()

        url = reverse_lazy('detail_club_application', kwargs={'pk': pk})
        return HttpResponseRedirect(url)


class DeleteApplication(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClubApplication
    # success_message = 'Pomyślnie usunięto zgłoszenie'

    #def delete(self, request, *args, **kwargs):
    #    messages.success(self.request, self.success_message % {'name': self.get_object().tournament.name})
    #    return super(DeleteTournamentMember, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('detail_club_application', kwargs={'pk': self.object.club.id})
