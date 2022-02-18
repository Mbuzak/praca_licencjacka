from django import forms
from .models import Tournament


class DateInput(forms.DateInput):
    input_type = 'date'


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = "__all__"
        widgets = {'start': DateInput(),
                   'end': DateInput(),
                   }
