from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import Club
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View
from accounts.models import Account
from joinment.models import Application


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
        context['members'] = Account.objects.filter(club_id=self.object.id).exclude(club__isnull=True)

        context['is_member'] = False
        if self.request.user.id in [member.id for member in context['members']]:
            context['is_member'] = True
        return context


class CreateClub(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    model = Club
    fields = ('name', 'email', 'place')
    template_name = 'clubs/create.html'
    success_url = reverse_lazy('home_club')
    permission_required = ('add_club',)

    def get_success_message(self, cleaned_data):
        return '%(name)s został pomyślnie utworzony' % {'name': self.object.name}

    def form_valid(self, form):
        form.instance.manager = Account.objects.get(pk=self.request.user.id)
        return super(CreateClub, self).form_valid(form)


class UpdateClub(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    model = Club
    template_name = 'clubs/update.html'
    fields = ('name', 'email', 'place')
    success_url = reverse_lazy('home_club')
    permission_required = ('change_club',)

    def get_success_message(self, cleaned_data):
        return '%(name)s został zaktualizowany' % {'name': self.object.name}


class DeleteClub(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Club
    success_url = reverse_lazy('home_club')
    success_message = '%(name)s został pomyślnie usunięty'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % {'name': self.get_object().name})
        return super(DeleteClub, self).delete(request, *args, **kwargs)


class AddMemberView(LoginRequiredMixin, SuccessMessageMixin, View):
    def post(self, request, pk):
        application = Application.objects.get(pk=pk)
        account = application.person
        account.club = application.club
        account.save()

        Application(pk=pk).delete()

        url = reverse_lazy('home_club')
        return HttpResponseRedirect(url)

    success_message = 'Pomyślnie dodano osobę do klubu'

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AddMemberView, self).dispatch(request, *args, **kwargs)


class ApplicationView(LoginRequiredMixin, DetailView):
    model = Club
    template_name = 'clubs/application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_application'] = Application.objects.filter(person_id=self.request.user.id, club_id=self.object.id,
                                                                type_of_object='C')
        context['applications'] = Application.objects.filter(club_id=self.object.id)
        return context


class CreateApplication(LoginRequiredMixin, View):
    def post(self, request, pk):
        Application(person_id=self.request.user.id, club_id=pk, type_of_object='C').save()

        url = reverse_lazy('detail_club_application', kwargs={'pk': pk})
        return HttpResponseRedirect(url)


class DeleteApplication(LoginRequiredMixin, DeleteView):
    model = Application

    def get_success_url(self):
        return reverse_lazy('detail_club_application', kwargs={'pk': self.object.club.id})


class LeaveClubView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Account
    fields = ('club',)
    success_message = 'Pomyślnie opuszczono klub'

    def get_success_url(self):
        return reverse_lazy('detail_club', kwargs={'pk': self.kwargs['club_id']})

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        request.POST['club'] = None
        return super(LeaveClubView, self).post(request, **kwargs)
