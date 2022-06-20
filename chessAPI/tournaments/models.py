import datetime
from chessAPI import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from ratings.models import TITLE, FIDE_TITLE, TITLE_TUPLE
from accounts.models import GENDER
from django.core.validators import RegexValidator


class Tournament(models.Model):
    GAME_TYPE_CHOICES = [
        ('błyskawiczny', 'błyskawiczny'),
        ('szybki', 'szybki'),
        ('klasyczny', 'klasyczny'),
    ]

    GAME_SYSTEM_CHOICES = [
        ('szwajcarski', 'szwajcarski'),
        ('kołowy(rundowy)', 'kołowy(rundowy)'),
    ]

    STATUS_CHOICES = [
        ('trwające', 'trwające'),
        ('zakończone', 'zakończone'),
        ('planowane', 'planowane'),
    ]

    name = models.CharField(verbose_name='Nazwa turnieju', max_length=100, unique=True, default='')
    start = models.DateField(verbose_name='Data rozpoczęcia', default=datetime.date.today)
    end = models.DateField(verbose_name='Data zakończenia', default=datetime.date.today)
    round_number = models.SmallIntegerField(verbose_name='Liczba rund', default=1, validators=[MinValueValidator(1)])

    game_rate = models.CharField(verbose_name='Tempo gry', max_length=10, default='')
    game_system = models.CharField(verbose_name='System rozgrywek', max_length=20, choices=GAME_SYSTEM_CHOICES,
                                   default='')
    game_type = models.CharField(verbose_name='Rodzaj gry', choices=GAME_TYPE_CHOICES, max_length=20, default='')
    is_polish_rated = models.BooleanField(verbose_name='Czy turniej jest zgłoszony do oceny PZSzach', default=False)

    place = models.CharField(verbose_name='Miejsce', max_length=100, blank=True, default='',
                             validators=[RegexValidator(r'\D*, \D*, .*', message='województwo, miasto, ulica')])
    organizer = models.CharField(verbose_name='Organizator', max_length=100, default='')
    judge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Sędzia', default='')

    is_started = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)

    description = models.TextField(verbose_name='Opis', max_length=255, blank=True,
                                   validators=[MaxLengthValidator(250)])

    def __str__(self):
        return self.name

    def status(self):
        if datetime.date.today() < self.start:
            return 'planowane'
        elif datetime.date.today() > self.end:
            return 'zakończone'
        return 'trwające'

    def count_members(self):
        return len(TournamentMember.objects.filter(tournament_id=self.pk))

    def get_province(self):
        if len(self.place) > 0:
            return self.place.split(',')[0]
        return ''

    def get_city(self):
        if len(self.place) > 0:
            return self.place.split(',')[1]
        return ''

    def get_street(self):
        if len(self.place) > 0:
            return self.place.split(',')[2]
        return ''


class TournamentMember(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    points = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    title = models.CharField(max_length=10)
    fide_rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.person.name + ' ' + self.person.lastname + ', ' + self.tournament.name

    def get_title(self):
        if self.title == 'b/k':
            return ''
        return self.title

    def get_rating(self):
        if self.title in TITLE_TUPLE:
            return TITLE[GENDER[self.person.gender]][self.title]
        return FIDE_TITLE[GENDER[self.person.gender]][self.title]


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.SmallIntegerField()

    def __str__(self):
        return str(self.pk)


class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    chessboard = models.SmallIntegerField()

    white = models.ForeignKey(TournamentMember, on_delete=models.CASCADE, related_name='match_white')
    black = models.ForeignKey(TournamentMember, on_delete=models.CASCADE, related_name='match_black')

    white_result = models.FloatField(verbose_name='Wynik', blank=True, null=True)
    black_result = models.FloatField(verbose_name='Wynik', blank=True, null=True)


class Promotion(models.Model):
    participant = models.OneToOneField(TournamentMember, on_delete=models.CASCADE, related_name='participant')
    title = models.CharField(max_length=10)
    status = models.BooleanField()
