from django.db import models

'''
from model_helpers import Choices


PROVINCE_CHOICES = Choices({
    'pomorskie': 'PO',
    'zachodnio-pomorskie': 'ZP',
    'kujawsko-pomorskie': 'KP',
    'warmińsko-mazurskie': 'WM',
    'mazowieckie': 'MA',
    'małopolskie': 'MP',
    'lubelskie': 'LU',
    'lubuskie': 'LB',
    'opolskie': 'OP',
    'dolnośląskie': 'DS',
    'śląskie': 'SL',
    'wielkopolskie': 'WP',
    'świętokrzyskie': 'SK',
    'podlaskie': 'PL',
    'łódzkie': 'LU',
    'podkarpackie': 'PK',
})

'''
class Address(models.Model):
    province = models.CharField(verbose_name='Województwo', max_length=20, default='')
    city = models.CharField(verbose_name='Miasto', max_length=50, default='')
    street = models.CharField(verbose_name='Ulica', max_length=50, default='')

    def __str__(self):
        return str(self.province) + ', ' + str(self.city) + ' ul. ' + str(self.street)
