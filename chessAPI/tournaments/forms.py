from django import forms
from .models import Tournament
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Button


class DateInput(forms.DateInput):
    input_type = 'date'


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'game_system', 'game_rate', 'game_type', 'is_fide', 'round_number',
                  'address', 'organizer')
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
                Column('address', css_class='form-group col-md-4 mb-4'),
                Column('organizer', css_class='form-group col-md-4'),
                css_class='form_row'
            ),
            Fieldset('co'),
            Button("{% url 'create_address' %}", 'create_address', css_class='btn btn-primary', onclick="{% url 'create_address' %}"),
            Row(
                Column('start', css_class='form-group col-md-3 mb-4'),
                Column('end', css_class='form-group col-md-3'),
                css_class='form_row'
            ),
            Row(
                Column('game_system', css_class='form-group col-md-2 mb-0'),
                Column('game_type', css_class='form-group col-md-2'),
                Column('game_rate', css_class='form-group col-md-2'),
                Column('round_number', css_class='form-group col-md-2'),
                css_class='form_row'
            ),
            Row(
                Column('is_fide', css_class='form-group col-md-5 mb-4'),
                css_class='form_row'
            ),
            Submit('submit', 'Zapisz')
        )
