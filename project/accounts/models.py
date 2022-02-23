# accounts/models.py
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from clubs.models import Club

GENDER_CHOICES = [
    ('M', 'mężczyzna'),
    ('K', 'kobieta'),
]


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, lastname, gender, born_year, country, city, password, **extra_fields):
        values = [email, name, lastname, gender, born_year, country, city]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, lastname=lastname, gender=gender, born_year=born_year,
                          country=country, city=city, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, lastname, gender, born_year, country, city, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, lastname, gender, born_year, country, city, password, **extra_fields)

    def create_superuser(self, email, name, lastname, gender, born_year, country, city, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, lastname, gender, born_year, country, city, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(verbose_name="Imię", max_length=150, default='')
    lastname = models.CharField(verbose_name="Nazwisko", max_length=150, default='')
    gender = models.CharField(verbose_name="Płeć", max_length=20, choices=GENDER_CHOICES, default='')
    born_year = models.IntegerField(verbose_name="Rok urodzenia", default=1970,
                                    validators=[MinValueValidator(1900), MaxValueValidator(2200)])
    country = models.CharField(verbose_name="Państwo", max_length=20, default='')
    city = models.CharField(verbose_name="Miasto", max_length=20, default='')

    picture = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, related_name='accounts')

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname', 'gender', 'born_year', 'country', 'city']

    def __str__(self):
        return self.name + " " + self.lastname

    #def get_full_name(self):
    #    return self.name

    #def get_short_name(self):
    #    return self.name.split()[0]
