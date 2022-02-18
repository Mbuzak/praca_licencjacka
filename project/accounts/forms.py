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
            'born_year',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.lastname = self.cleaned_data['lastname']
        user.born_year = self.cleaned_data['born_year']

        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('email',
                  'name',
                  'lastname',
                  'born_year',
                  'password')
