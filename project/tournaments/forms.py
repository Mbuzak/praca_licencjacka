from django import forms
from .models import *
from addresses.models import PROVINCE_CHOICES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class DateInput(forms.DateInput):
    input_type = 'date'


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'game_rate', 'game_system', 'game_type', 'round_count', 'is_fide',
                  'address', 'organizer', 'judge')
        widgets = {'start': DateInput(),
                   'end': DateInput(),
                   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-5 mb-4'),
                css_class='form_row'
            ),
            Row(
                Column('start', css_class='form-group col-md-3 mb-4'),
                Column('end', css_class='form-group col-md-3 mb-4'),
                css_class='form_row'
            ),
            Row(
                Column('game_system', css_class='form-group col-md-3 mb-0'),
                Column('game_type', css_class='form-group col-md-3 mb-0'),
                Column('game_rate', css_class='form-group col-md-2 mb-0'),
                Column('round_count', css_class='form-group col-md-2 mb-0'),
                css_class='form_row'
            ),
            Row(
                Column('is_fide', css_class='form-group col-md-5 mb-4'),
                css_class='form_row'
            ),
            'address',
            Row(
                Column('judge', css_class='form-group col-md-4 mb-0'),
                Column('organizer', css_class='form-group col-md-4 mb-0'),
                css_class='form_row'
            ),
            Submit('submit', 'Zapisz')
        )


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
