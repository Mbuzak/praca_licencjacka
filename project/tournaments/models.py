import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from chessAPI import settings
import model_helpers


PROVINCE_CHOICES = [
    ('pomorskie', 'PO'),
    ('zachodnio-pomorskie', 'ZP'),
    ('kujawsko-pomorskie', 'KP'),
    ('warmińsko-mazurskie', 'WM'),
    ('mazowieckie', 'MA'),
    ('małopolskie', 'MP'),
    ('lubelskie', 'LU'),
    ('lubuskie', 'LB'),
    ('opolskie', 'OP'),
    ('dolnośląskie', 'DS'),
    ('śląskie', 'SL'),
    ('wielkopolskie', 'WP'),
    ('świętokrzyskie', 'SK'),
    ('podlaskie', 'PL'),
    ('łódzkie', 'LU'),
    ('podkarpackie', 'PK'),
]

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


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(verbose_name='Kraj', max_length=50, default='')
    province = models.CharField(verbose_name='Województwo', max_length=20, default='', choices=PROVINCE_CHOICES)
    city = models.CharField(verbose_name='Miasto', max_length=50, default='')
    street = models.CharField(verbose_name='Ulica', max_length=100, default='')
    house_number = models.IntegerField(verbose_name='Numer domu', default=1,
                                       validators=[MaxValueValidator(500), MinValueValidator(1)])

    def __str__(self):
        return str(self.province) + ', ' + str(self.city)


class Tournament(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Nazwa turnieju', max_length=100, unique=True, default='')
    start = models.DateField(verbose_name='Data rozpoczęcia', default=datetime.date.today)
    end = models.DateField(verbose_name='Data zakończenia', default=datetime.date.today)

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
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


# Player can create/delete application
# Tournament's judge can accept(TournamentMember) or refuse players application
class TournamentApplication(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
