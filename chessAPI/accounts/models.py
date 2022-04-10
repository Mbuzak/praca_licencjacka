from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from clubs.models import Club
from ratings.models import TITLE_CHOICES, TITLE, THRESHOLD, TITLE_TUPLE
from addresses.models import PROVINCE_CHOICES


GENDER_CHOICES = [
    ('M', 'mężczyzna'),
    ('K', 'kobieta'),
]


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, lastname, gender, born_year, province, password, **extra_fields):
        values = [email, name, lastname, gender, born_year, province]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, lastname=lastname, gender=gender, born_year=born_year,
                          province=province, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        g = Group.objects.get(name='Judge')
        p = Permission.objects.get(codename='add_tournament')
        user.groups.add(g)
        user.user_permissions.add(p)
        return user

    def create_user(self, email, name, lastname, gender, born_year, province, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, lastname, gender, born_year, province, password, **extra_fields)

    def create_superuser(self, email, name, lastname, gender, born_year, province, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, lastname, gender, born_year, province, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(verbose_name="Imię", max_length=50, default='')
    lastname = models.CharField(verbose_name="Nazwisko", max_length=50, default='')
    gender = models.CharField(verbose_name="Płeć", max_length=10, choices=GENDER_CHOICES, default='')
    born_year = models.IntegerField(verbose_name="Rok urodzenia", default=1970,
                                    validators=[MinValueValidator(1900), MaxValueValidator(2200)])

    province = models.CharField(verbose_name='Województwo', max_length=20, default='', blank=True,
                                choices=PROVINCE_CHOICES())
    picture = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True, default=None,
                             related_name='accounts')
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default='b/k')

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname', 'gender', 'born_year', 'province']

    def __str__(self):
        return self.name + " " + self.lastname

    def get_category(self):
        if self.title == 'b/k':
            return ''
        return self.title

    def get_polish_rating(self):
        if self.gender == 'M':
            return TITLE['male'][self.title]
        return TITLE['female'][self.title]

    def next_category(self):
        next_pos = TITLE_TUPLE.index(self.title) + 1
        if len(TITLE_TUPLE) == next_pos:
            print('WARNING!!!') # TBD
            return -1
        else:
            return TITLE_TUPLE[next_pos]

    def next_threshold(self):
        next_category = self.next_category()
        if next_category != -1:
            if self.gender == 'M':
                return THRESHOLD['male'][next_category]
            return THRESHOLD['female'][next_category]
        else:
            print('WARNING') # tbd
            return -1
