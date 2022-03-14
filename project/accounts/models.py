from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from clubs.models import Club
from country_list import countries_for_language
from ratings.models import TITLE_CHOICES, TITLE
from addresses.models import PROVINCE_CHOICES
from ratings.models import FideRating


GENDER_CHOICES = [
    ('M', 'mężczyzna'),
    ('K', 'kobieta'),
]

COUNTRY_CHOICES = countries_for_language('pl')


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, lastname, gender, born_year, country, password, **extra_fields):
        values = [email, name, lastname, gender, born_year, country]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, lastname=lastname, gender=gender, born_year=born_year,
                          country=country, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, lastname, gender, born_year, country, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, lastname, gender, born_year, country, password, **extra_fields)

    def create_superuser(self, email, name, lastname, gender, born_year, country, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, lastname, gender, born_year, country, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(verbose_name="Imię", max_length=150, default='')
    lastname = models.CharField(verbose_name="Nazwisko", max_length=150, default='')
    gender = models.CharField(verbose_name="Płeć", max_length=20, choices=GENDER_CHOICES, default='')
    born_year = models.IntegerField(verbose_name="Rok urodzenia", default=1970,
                                    validators=[MinValueValidator(1900), MaxValueValidator(2200)])
    country = models.CharField(verbose_name="Państwo", max_length=20, choices=COUNTRY_CHOICES,
                               default=COUNTRY_CHOICES[165])

    province = models.CharField(verbose_name='Ewidencja WZSzach', max_length=20, default='', blank=True,
                                choices=PROVINCE_CHOICES())
    city = models.CharField(verbose_name="Miasto", max_length=20, default='', blank=True)
    picture = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, related_name='accounts')
    category = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True, null=True)  # TBD

    fide_number = models.CharField(max_length=20, blank=True, null=True, default=None)
    fide = models.ForeignKey(FideRating, related_name='accounts', on_delete=models.CASCADE, null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname', 'gender', 'born_year', 'country']

    def __str__(self):
        return self.name + " " + self.lastname

    def get_id_cr(self):
        return 'PL-' + str(self.pk)

    def get_category(self):
        if self.category == 'b/k':
            return ''
        return self.category

    def get_polish_rating(self):
        if self.gender == 'M':
            return TITLE['male'][self.category]
        return TITLE['female'][self.category]

    def get_fide_number(self):
        return self.fide_number if self.fide_number else ''
