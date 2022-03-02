import django_filters
import models


class TournamentFilter(django_filters.FilterSet):
    class Meta:
        model = models.Tournament
        fields = {
            'start': ['lt', 'gt'],
        }