from django.contrib.auth.models import Permission, Group
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, View
from .forms import RegisterForm
from .models import Account
from tournaments.models import TournamentMember, Promotion
from ratings.models import FideHistory, FidePeriod
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import datetime
from tournaments.pairing_system import verify_promotion


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class IndexView(ListView):
    model = Account
    template_name = 'accounts/index.html'
    # context_object_name = 'tournaments'
    # paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['latest_period'] = True
        latest_period = FidePeriod.objects.latest('year', 'month')
        if latest_period.month == datetime.now().month and latest_period.year == datetime.now().year:
            context['latest_period'] = False
        context['promotions'] = Promotion.objects.filter(status=False)

        return context


class ProfileView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tournaments'] = TournamentMember.objects.filter(person=self.kwargs['pk'])
        context['fide_history'] = FideHistory.objects.filter(person_id=self.kwargs['pk'])
        history = TournamentMember.objects.filter(person=self.kwargs['pk'],
                                                  tournament__is_ended=True).order_by('tournament__start', 'tournament__end')[0:5]
        context['latest_tournaments'] = history

        print(self.request.user)

        #u = Account.objects.get(pk=self.request.user.id)
        u = Account.objects.get(pk=13)
        g = Group.objects.get(name='Judge')
        p = Permission.objects.get(name='Can add tournament')

        print(p)
        print(u.get_user_permissions())
        for g in u.groups.all():
            print(g.name)
            print(g.permissions.all())

        print('!!!')
        print('judge', u.is_judge())
        print('engineer', u.is_WZSzach_engineer())
        print('instructor', u.is_instructor())

        print(u.has_perm('tournaments.add_tournament'))
        print(u.has_perm('tournaments.create_tournament'))
        print(u.has_perm(p))
        return context


class UpdateCategory(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('change_promotion',)

    def get(self, request, pk):
        promotion = Promotion.objects.get(pk=pk)
        verify_promotion(promotion)

        url = reverse_lazy('home_accounts')
        return HttpResponseRedirect(url)
