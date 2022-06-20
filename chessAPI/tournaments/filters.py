import django_filters
from .models import Tournament as To
from django import forms
from datetime import datetime


class TournamentFilter(django_filters.FilterSet):

    game_type_filter = django_filters.ChoiceFilter(label='Typ gry', choices=To.GAME_TYPE_CHOICES, method='game_type_filtering')
    status_filter = django_filters.ChoiceFilter(label='Status', choices=To.STATUS_CHOICES, method='status_filtering')
    game_system_filter = django_filters.ChoiceFilter(label='System', choices=To.GAME_SYSTEM_CHOICES, method='game_system_filtering')
    polish_rated_filter = django_filters.BooleanFilter(label='PZSzach', method='polish_rated_filtering', widget=forms.CheckboxInput())
    year_filter = django_filters.ChoiceFilter(label='Rok', method='year_filtering',
                                              choices=list(set([(x.start.year, x.start.year) for x in To.objects.all()])))

    class Meta:
        model = To
        fields = []

    def game_type_filtering(self, queryset, name, value):
        return queryset.filter(game_type=value)

    def status_filtering(self, queryset, name, value):
        id_list = [x.id for x in queryset.all() if x.status() == value]
        print(value, id_list)
        return queryset.filter(id__in=id_list)

    def game_system_filtering(self, queryset, name, value):
        return queryset.filter(game_system=value)

    def polish_rated_filtering(self, queryset, name, value):
        if value:
            return queryset.filter(is_polish_rated=value)
        return queryset.all()

    def year_filtering(self, queryset, name, value):
        id_list = [x.id for x in queryset.all() if x.start.year == int(value)]
        return queryset.filter(id__in=id_list)
