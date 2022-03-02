import datetime
from chessAPI import settings
import model_helpers
from addresses.models import *


GAME_TYPE_CHOICES = [
    ('blitz', 'błyskawiczne'),
    ('rapid', 'szybkie'),
    ('classic', 'klasyczne'),
]

GAME_SYSTEM_CHOICES = [
    ('szwajcarski', 'szwajcarski'),
    ('kołowy(rundowy)', 'kołowy(rundowy)'),
    ('arena', 'arena'),
]


TITLE_CHOICES = [
    ('b/k', 'b/k'),
    ('V', 'V'),
    ('IV', 'IV'),
    ('III', 'III'),
    ('II', 'II'),
    ('II+', 'II+'),
    ('I', 'I'),
    ('I+', 'I+'),
    ('I++', 'I++'),
    ('k', 'k'),
    ('m', 'm'),
]


MALE_TITLES = {'b/k': 1000,
               'V': 1200,
               'IV': 1400,
               'III': 1600,
               'II': 1800,
               'II+': 1900,
               'I': 2000,
               'I+': 2100,
               'I++': 2100,
               'k': 2200,
               'k+': 2300,
               'k++': 2300,
               'm': 2400,
               }


FEMALE_TITLES = {'b/k': 1000,
               'V': 1100,
               'IV': 1250,
               'III': 1400,
               'II': 1600,
               'II+': 1700,
               'I': 1800,
               'I+': 1900,
               'I++': 1900,
               'k': 2000,
               'k+': 2100,
               'k++': 2100,
               'm': 2200,
               }


class Tournament(models.Model):
    name = models.CharField(verbose_name='Nazwa turnieju', max_length=100, unique=True, default='')
    start = models.DateField(verbose_name='Data rozpoczęcia', default=datetime.date.today)
    end = models.DateField(verbose_name='Data zakończenia', default=datetime.date.today)
    round_count = models.IntegerField(verbose_name='Liczba rund', default=1, validators=[MinValueValidator(1),
                                                                                         MaxValueValidator(30)])

    game_rate = models.CharField(verbose_name='Tempo gry', max_length=10, default='')
    game_system = models.CharField(verbose_name='System rozgrywek', max_length=20, choices=GAME_SYSTEM_CHOICES,
                                   default='')
    game_type = models.CharField(verbose_name='Rodzaj gry', choices=GAME_TYPE_CHOICES, max_length=20, default='')
    is_fide = models.BooleanField(verbose_name='Czy turniej jest rankingowy FIDE?', default=False)

    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Adres')

    organizer = models.CharField(verbose_name='Organizator', max_length=100, default='')
    judge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Sędzia', default='')

    def __str__(self):
        return self.name

    def status(self):
        if datetime.date.today() < self.start:
            return '#00aa00'  # coming soon
        elif datetime.date.today() > self.end:
            return '#ff0000'  # completed
        else:
            return '#0000ff'  # active


class TournamentMember(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class TournamentApplication(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.IntegerField()


class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    chessboard = models.IntegerField()
    # players
    white = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='match_white')
    black = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='match_black')
    # results
    white_result = models.CharField(max_length=20, default='', blank=True)
    black_result = models.CharField(max_length=20, default='', blank=True)
