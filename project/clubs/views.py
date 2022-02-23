import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView

from chessAPI import settings
from .models import Club, ClubMember
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, DetailView, View


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


class CreateClubMember(LoginRequiredMixin, SuccessMessageMixin, View):
    model = Club
    def get(self, request, *args, **kwargs):
        # self.object = self.get_object()
        # ClubMember(person_id=request.user.id, club_id=Club.objects.get(pk=self.object.id)).save()
        ClubMember(person_id=request.user.id, club_id=Club.objects.get(pk=kwargs['pk']).id).save()
        return HttpResponseRedirect('/clubs')

    success_message = 'Pomyślnie dołączono do klubu %(name)s'

    def dispatch(self, request, *args, **kwargs):
        # self.object = self.get_object()
        # messages.success(self.request, self.success_message % {'name': Club.objects.get(name=self.object)})
        # messages.success(self.request, self.success_message % {'name': request.club.name})
        messages.success(self.request, self.success_message % {'name': Club.objects.get(pk=kwargs['pk'])})
        return super(CreateClubMember, self).dispatch(request, *args, **kwargs)


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

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        request.POST['leave'] = datetime.date.today()
        return super(LeaveClub, self).post(request, **kwargs)





