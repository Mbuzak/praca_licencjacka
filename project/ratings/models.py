from django.db import models
from chessAPI import settings
import datetime


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

TITLE_TUPLE = ('b/k', 'V', 'IV', 'III', 'II', 'II+', 'I', 'I+', 'I++', 'k', 'm')


TITLE = {'male': {'b/k': 1000, 'V': 1200, 'IV': 1400, 'III': 1600, 'II': 1800, 'II+': 1900, 'I': 2000, 'I+': 2100,
                  'I++': 2100, 'k': 2200, 'k+': 2300, 'k++': 2300, 'm': 2400},
         'female': {'b/k': 1000, 'V': 1100, 'IV': 1250, 'III': 1400, 'II': 1600, 'II+': 1700, 'I': 1800, 'I+': 1900,
                    'I++': 1900, 'k': 2000, 'k+': 2100, 'k++': 2100, 'm': 2200}
         }

THRESHOLD = {
        'male': {'V': 1050, 'IV': 1300, 'III': 1550, 'II': 1800, 'II+': 1900, 'I': 2000, 'I+': 2100,
                 'I++': 2100, 'k': 2200, 'k+': 2300, 'k++': 2300, 'm': 2400},
        'female': {'V': 1000, 'IV': 1150, 'III': 1350, 'II': 1600, 'II+': 1700, 'I': 1800, 'I+': 1900,
                   'I++': 1900, 'k': 2000, 'k+': 2100, 'k++': 2100, 'm': 2200}
}


class FidePeriod(models.Model):
    change = models.DateTimeField(default=datetime.datetime.now)
    month = models.SmallIntegerField(default=datetime.date.today().month)
    year = models.SmallIntegerField(default=datetime.date.today().year)


class FideRating(models.Model):
    classic = models.SmallIntegerField(blank=True, null=True)
    rapid = models.SmallIntegerField(blank=True, null=True)
    blitz = models.SmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=30, default=None, blank=True, null=True)

    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class FideHistory(models.Model):
    classic = models.SmallIntegerField()
    rapid = models.SmallIntegerField()
    blitz = models.SmallIntegerField()

    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    period = models.ForeignKey(FidePeriod, on_delete=models.CASCADE, default='', blank=True, null=True)
