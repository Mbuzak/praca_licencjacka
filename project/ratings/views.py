from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from .models import FideRating, FideHistory, FidePeriod
from accounts.models import Account
import requests
import re
from selectolax.parser import HTMLParser
import datetime


class CreateFideView(View):
    def get(self, request):
        def is_new_period():
            if FidePeriod.objects.all():
                today = datetime.date.today()
                latest_period = FidePeriod.objects.latest('change')
                if latest_period.year == today.year and latest_period.month == today.month:
                    return False
            return True

        def create_period():
            FidePeriod().save()

        def fide_accounts():
            return Account.objects.exclude(fide_number__isnull=True)

        def update_fide_history(account):
            latest_period = FidePeriod.objects.latest('change')

            if FideRating.objects.filter(person_id=account.id):
                rating = FideRating.objects.get(person_id=account.id)

                FideHistory(classic=rating.classic, rapid=rating.rapid, blitz=rating.blitz,
                            person_id=account.id, period_id=latest_period.id).save()

        def update_fide(account):
            path = requests.get(f'https://ratings.fide.com/profile/{account.fide_number}').text
            parser = HTMLParser(html=path)
            parsed_text = parser.css('.profile-top-rating-dataCont')[0].text().strip()
            regex_text = re.split(r'\s{2,}', parsed_text)

            for i in [1, 3, 5]:
                if regex_text[i] == 'Not rated':
                    regex_text[i] = 0

            parsed_title = parser.css('.profile-top-info__block__row__data')[-1].text()
            title = None
            if parsed_title != 'None':
                title = parsed_title

            if FideRating.objects.filter(person_id=account.id):
                fide_rating = FideRating.objects.get(person_id=account.id)
                fide_rating.classic = regex_text[1]
                fide_rating.rapid = regex_text[3]
                fide_rating.blitz = regex_text[5]
                fide_rating.save()
            else:
                FideRating(classic=regex_text[1], rapid=regex_text[3], blitz=regex_text[5],
                           title=title, person_id=account.id).save()
                fide_rating = FideRating.objects.get(person_id=account.id)
                account_edit = Account.objects.get(pk=account.id)
                account_edit.fide_id = fide_rating.id
                account_edit.save()

        if is_new_period():
            create_period()

            for acc in fide_accounts():
                update_fide_history(acc)
                update_fide(acc)

        url = reverse_lazy('home_accounts')
        return HttpResponseRedirect(url)
