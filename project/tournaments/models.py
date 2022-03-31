import datetime
from chessAPI import settings
import model_helpers
from addresses.models import Address
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


GAME_TYPE_CHOICES = [
    ('błyskawiczny', 'blitz'),
    ('szybki', 'rapid'),
    ('klasyczny', 'classic'),
]

GAME_SYSTEM_CHOICES = [
    ('szwajcarski', 'szwajcarski'),
    ('kołowy(rundowy)', 'kołowy(rundowy)'),
    ('arena', 'arena'),
]


class Tournament(models.Model):
    name = models.CharField(verbose_name='Nazwa turnieju', max_length=100, unique=True, default='')
    start = models.DateField(verbose_name='Data rozpoczęcia', default=datetime.date.today)
    end = models.DateField(verbose_name='Data zakończenia', default=datetime.date.today)
    round_number = models.IntegerField(verbose_name='Liczba rund', default=1, validators=[MinValueValidator(1)])

    game_rate = models.CharField(verbose_name='Tempo gry', max_length=10, default='')
    game_system = models.CharField(verbose_name='System rozgrywek', max_length=20, choices=GAME_SYSTEM_CHOICES,
                                   default='')
    game_type = models.CharField(verbose_name='Rodzaj gry', choices=GAME_TYPE_CHOICES, max_length=20, default='')
    is_fide = models.BooleanField(verbose_name='Czy turniej jest rankingowy FIDE', default=False)

    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Adres', blank=True, null=True) # remove null&blank
    organizer = models.CharField(verbose_name='Organizator', max_length=100, default='')
    judge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Sędzia', default='')

    is_started = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def status(self):
        if datetime.date.today() < self.start:
            return 'coming soon'
        elif datetime.date.today() > self.end:
            return 'ended'
        return 'ongoing'

    def color_status(self):
        colors = {'ongoing': '#0000bb', 'ended': '#bb0000', 'coming soon': '#00bb00'}
        return colors[self.status()]


class TournamentMember(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    points = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.IntegerField()

    def __str__(self):
        return str(self.pk)


class Match(models.Model):
    GAME_RESULT_CHOICES = [
        ('1', '1'),
        ('0.5', '0.5'),
        ('0', '0'),
        ('+', '+'),
        ('-', '-'),
    ]

    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    chessboard = models.IntegerField()

    white = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='match_white')
    black = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='match_black')

    white_result = models.CharField(max_length=20, choices=GAME_RESULT_CHOICES)
    black_result = models.CharField(max_length=20, choices=GAME_RESULT_CHOICES)
