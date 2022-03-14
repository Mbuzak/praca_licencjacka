from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login, authenticate
from accounts.models import Account


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Account
        fields = (
            'email',
            'name',
            'lastname',
            'gender',
            'born_year',
            'country',
            'province',
            'city',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.lastname = self.cleaned_data['lastname']
        user.gender = self.cleaned_data['gender']
        user.born_year = self.cleaned_data['born_year']
        user.country = self.cleaned_data['country']
        user.province = self.cleaned_data['province']
        user.city = self.cleaned_data['city']

        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('email',
                  'name',
                  'lastname',
                  'gender',
                  'born_year',
                  'country',
                  'province',
                  'city',
                  'password',
                  )

