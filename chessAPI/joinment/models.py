from django.db import models
from chessAPI import settings
from clubs.models import Club
from tournaments.models import Tournament


OBJECT_CHOICES = [
    ('C', 'Club'),
    ('T', 'Tournament'),
]


class Application(models.Model):
    type_of_object = models.CharField(max_length=1, choices=OBJECT_CHOICES)

    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True, related_name='application')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, blank=True, null=True, related_name='application')
