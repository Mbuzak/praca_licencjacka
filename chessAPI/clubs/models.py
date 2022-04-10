import datetime
from django.db import models
from chessAPI import settings
from addresses.models import Address


class Club(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa klubu", max_length=50, unique=True, default='')
    email = models.EmailField(max_length=255, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Adres')
    registration = models.DateField(verbose_name='Data założenia', default=datetime.date.today)  # format
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Menadżer",
                                related_name='clubs')

    def __str__(self):
        return self.name
