from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'




class TournamentForm(forms.ModelForm):
    # address = forms.ModelChoiceField(queryset=Address.objects.all())
    province = forms.ModelChoiceField(queryset=Address.objects.values_list('province', flat=True))
    print(province, province.queryset, province.widget)
    city = forms.ModelChoiceField(queryset=Address.objects.filter(province=province.label),
                                  )
    # city = forms.ModelChoiceField(queryset=Address.objects.none())
    # city = forms.CharField(max_length=50)]

    class Meta:
        model = Tournament
        # fields = "__all__"
        fields = ('name', 'start', 'end', 'game_rate', 'game_system', 'game_type', 'is_fide', 'province', 'city')
        widgets = {'start': DateInput(),
                   'end': DateInput(),
                   }
