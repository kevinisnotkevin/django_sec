from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

from.models import User


class SignUpForm(UserCreationForm):
    error_messages = {
        "password_mismatch": "Пароли не совпадают.",
    }
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username", "email")
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }


class LoginForm(forms.Form):
    email = forms.CharField(label="Почта")
    password = forms.CharField(label="Пароль")


class EditProfileForm(forms.Form):
    username = forms.CharField()
    about = forms.CharField(widget=forms.Textarea())
    image = forms.ImageField(required=False)

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.original_username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(
                    'Имя пользователя занято.')
        return username