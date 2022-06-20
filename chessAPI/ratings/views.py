from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from .models import FideRating, FideHistory, FidePeriod
from accounts.models import Account
import requests
import re
from selectolax.parser import HTMLParser
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


FIDE = {'International Master': 'IM',
        'FIDE Master': 'FM',
        'Grandmaster': 'GM',
        'Woman Intl. Master': 'WIM',
        'Woman Grandmaster': 'WGM',
        'Candidate Master': 'CM',
        'Woman FIDE Master': 'WFM',
        'Woman Candidate Master': 'WCM',
        }


def is_new_period():
    if FidePeriod.objects.all():
        today = datetime.date.today()
        latest_period = FidePeriod.objects.latest('change')
        if latest_period.year == today.year and latest_period.month == today.month:
            return False
    return True


def update_fide_history(fide_rating):
    latest_period = FidePeriod.objects.latest('change')

    FideHistory(classic=fide_rating.classic, rapid=fide_rating.rapid, blitz=fide_rating.blitz,
                person_id=fide_rating.person.id, period_id=latest_period.id).save()


def fide_profile(number):
    path = requests.get(f'https://ratings.fide.com/profile/{number}').text
    parser = HTMLParser(html=path)
    try:
        parsed_text = parser.css('.profile-top-rating-dataCont')[0].text().strip()
    except IndexError:
        print('taki numer nie istnieje')
        return -1

    regex_text = re.split(r'\s{2,}', parsed_text)

    for i in [1, 3, 5]:
        if regex_text[i] == 'Not rated':
            regex_text[i] = 0

    parsed_title = parser.css('.profile-top-info__block__row__data')[-1].text()

    regex_text.append(parsed_title)
    return regex_text


def update_fide(fide_rating):
    profile = fide_profile(fide_rating.fide_number)

    if profile == -1:
        return -1

    fide_rating.classic = profile[1]
    fide_rating.rapid = profile[3]
    fide_rating.blitz = profile[5]
    fide_rating.save()

    if profile[6] != 'None':
        account = fide_rating.person
        account.title = FIDE[profile[6]]
        account.save()


class UpdateFidePeriodView(LoginRequiredMixin, View):
    def get(self, request):
        if is_new_period():
            FidePeriod().save()

            for rating in FideRating.objects.all():
                update_fide_history(rating)
                update_fide(rating)

        url = reverse_lazy('home_accounts')
        return HttpResponseRedirect(url)


class CreateFideView(LoginRequiredMixin, CreateView):
    model = FideRating
    fields = ('fide_number',)
    template_name = 'ratings/create_fide.html'
    success_url = reverse_lazy('home_accounts')

    def form_valid(self, form):
        account = Account.objects.get(pk=self.kwargs['pk'])
        form.instance.person = account

        profile = fide_profile(form.instance.fide_number)

        if profile == -1 or form.instance.fide_number in [obj.fide_number for obj in FideRating.objects.all()]:
            return super(CreateFideView, self).form_invalid(form)

        form.instance.classic = profile[1]
        form.instance.rapid = profile[3]
        form.instance.blitz = profile[5]

        if profile[6] != 'None':
            account.title = FIDE[profile[6]]
            account.save()

        return super(CreateFideView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = Account.objects.get(pk=self.kwargs['pk'])
        return context
