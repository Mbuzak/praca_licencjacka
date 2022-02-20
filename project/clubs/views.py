from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
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
        context['club'] = Club.objects.get()
        context['members'] = ClubMember.objects.all()  # id_club, not all
        return context


class CreateClub(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Club
    fields = '__all__'
    # form_class = TournamentForm
    template_name = 'clubs/create.html'
    success_url = reverse_lazy('home')

    def get_success_message(self, cleaned_data):
        return '%(name)s został pomyślnie utworzony' % {'name': self.object.name}


class UpdateClub(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Club
    template_name = 'clubs/update.html'
    fields = ('name', 'email', 'id_manager',)
    success_url = reverse_lazy('home')

    def get_success_message(self, cleaned_data):
        return '%(name)s został zaktualizowany' % {'name': self.object.name}


class DeleteClub(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Club
    template_name = 'clubs/delete.html'
    success_url = reverse_lazy('home')
    success_message = '%(name)s został pomyślnie usunięty'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': self.get_object().name})
        return super(DeleteClub, self).delete(request, *args, **kwargs)


class CreateClubMember(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, *args, **kwargs):
        ClubMember(id_person_id=request.user.id, id_club_id=Club.objects.get().id).save()
        return HttpResponseRedirect('/clubs')

    success_message = 'Pomyślnie dołączono do klubu %(name)s'

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': Club.objects.get().name})
        return super(CreateClubMember, self).dispatch(request, *args, **kwargs)


class DeleteClubMember(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClubMember
    # template_name = 'tournaments/leave.html'
    # fields = '__all__'
    success_url = reverse_lazy('home')

    success_message = 'Pomyślnie opuszczono klub %(name)s'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': self.get_object().id_club.name})
        return super(DeleteClubMember, self).delete(request, *args, **kwargs)
