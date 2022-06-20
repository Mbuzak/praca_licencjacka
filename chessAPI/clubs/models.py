import datetime
from django.db import models
from chessAPI import settings
from django.core.validators import RegexValidator
from django.apps import apps


class Club(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa klubu", max_length=50, unique=True, default='')
    email = models.EmailField(max_length=255, unique=True)
    #address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Adres')
    place = models.CharField(verbose_name='Miejsce', max_length=100, blank=True, default='',
                             validators=[RegexValidator(r'\D*, \D*, .*', message='województwo, miasto, ulica')])
    registration = models.DateField(verbose_name='Data założenia', default=datetime.date.today)  # format
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Menadżer",
                                related_name='clubs')

    def __str__(self):
        return self.name

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

    def count_members(self):
        return len(apps.get_model('accounts', 'Account').objects.filter(club_id=self.pk))
