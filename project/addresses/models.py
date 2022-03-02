from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from model_helpers import Choices

PROVINCE_CHOICES2 = [
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


class Address(models.Model):
    province = models.CharField(verbose_name='Województwo', max_length=20, default='', choices=PROVINCE_CHOICES())
    city = models.CharField(verbose_name='Miasto', max_length=50, default='')
    street = models.CharField(verbose_name='Ulica', max_length=100, default='')
    house_number = models.IntegerField(verbose_name='Numer domu', default=1,
                                       validators=[MaxValueValidator(500), MinValueValidator(1)])

    def __str__(self):
        return str(self.province) + ', ' + str(self.city) + ' ul. ' + str(self.street) + ' ' + str(self.house_number)
