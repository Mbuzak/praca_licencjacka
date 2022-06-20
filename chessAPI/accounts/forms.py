from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login, authenticate
from accounts.models import Account
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Account
        fields = ('email', 'name', 'lastname', 'gender', 'born_year', 'province', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6'),
                css_class='form_row'
            ),
            Row(
                Column('name', css_class='form-group col-md-5'),
                Column('lastname', css_class='form-group col-md-4'),
                css_class='form_row'
            ),
            Row(
                Column('gender', css_class='form-group col-md-4'),
                Column('born_year', css_class='form-group col-md-4'),
                Column('province', css_class='form-group col-md-4'),
                css_class='form_row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-4'),
                css_class='form_row'
            ),
            Submit('submit', 'Zarejestruj się')
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.lastname = self.cleaned_data['lastname']
        user.gender = self.cleaned_data['gender']
        user.born_year = self.cleaned_data['born_year']
        user.province = self.cleaned_data['province']

        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('email', 'name', 'lastname', 'gender', 'born_year', 'province', 'password',)
