from django.db import models
import model_helpers
from chessAPI import settings
from tournaments.models import Tournament


POLISH_RATING_CHOICES = [{
    'male': {
        'bk': 1000,
        'V': 1200,

    },
    'female': {

    },
}]


class PolishRating(models.Model):
    name = models.CharField(verbose_name="Kategoria", max_length=20)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Osoba')
    obtain = models.DateField(verbose_name='Data zdobycia')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name='Turniej')
