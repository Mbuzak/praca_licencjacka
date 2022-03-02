from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class TournamentForm(forms.ModelForm):
    address = forms.ModelChoiceField(queryset=Address.objects.all(), label='Adres')
    # province = forms.ModelChoiceField(queryset=Address.objects.values_list('province', flat=True))
    # print(province, province.queryset, province.widget)
    # city = forms.ModelChoiceField(queryset=Address.objects.filter(province=province.label),
    #                               )
    # city = forms.ModelChoiceField(queryset=Address.objects.none())
    # city = forms.CharField(max_length=50)]

    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'game_rate', 'game_system', 'game_type', 'round_count', 'is_fide',
                  'address')
        widgets = {'start': DateInput(),
                   'end': DateInput(),
                   }


RESULT_CHOICES = [
    ('1', 'win'),
    ('0', 'lose'),
    ('0.5', 'draw'),
]


class MatchForm(forms.ModelForm):
    # white_result = forms.ModelChoiceField(widget=forms.Select(choices=RESULT_CHOICES))
    # white_result = forms.ChoiceField(choices=[1, 2, 3])
    # white_result = forms.DateField()
    # white_result = forms.ChoiceField(widget=forms.Select(choices=[1, 2, 3]))
    class Meta:
        model = Match
        fields = ('white_result', 'black_result')
