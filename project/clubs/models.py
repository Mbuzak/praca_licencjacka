import datetime

from django.db import models
from accounts.models import Account
from tournaments.models import Address


class Club(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa klubu", max_length=50, default='')
    email = models.EmailField(max_length=255, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Adres")
    registration = models.DateField(verbose_name='Data założenia', default=datetime.date.today)  # format
    id_manager = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Menadżer")

    def __str__(self):
        return self.name


class ClubMember(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_person = models.ForeignKey(Account, on_delete=models.CASCADE)
    id_club = models.ForeignKey(Club, on_delete=models.CASCADE)
    # join = models.DateField(verbose_name="Data dołączenia", default=datetime.date.today)
    # leave = models.DateField(verbose_name="Data opuszczenia", null=True, default='')
