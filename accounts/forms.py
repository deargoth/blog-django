from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User
from utils import site_messages


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        help_text='Digite sua senha',
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        help_text='Digite sua senha',
        label='Confirme sua senha'
    )

    def clean(self):
        data = self.cleaned_data

        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        password2 = data.get('password2')

        email_db = User.objects.filter(email=email).exists()

        if len(first_name) <= 3:
            self.add_error('first_name',
                           site_messages.error['register_form_first_name_too_short'])

        if len(last_name) <= 3:
            self.add_error('last_name',
                           site_messages.error['register_form_last_name_too_short'])

        if email_db:
            self.add_error('email',
                           site_messages.error['register_form_email_in_use'])

        if password != password2:
            raise ValidationError(
                site_messages.error['register_form_password_mismatch'])

        try:
            validate_password(password)

        except forms.ValidationError as error:
            self.add_error('password2',
                           error)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
    )

    def clean(self):
        data = self.cleaned_data

        email = data.get('email')
        email_db = User.objects.filter(email=email).exists()

        if not email_db:
            self.add_error('email',
                           site_messages.error['login_inexistent_email'])

    class Meta:
        model = User
        fields = ('email', 'password')
