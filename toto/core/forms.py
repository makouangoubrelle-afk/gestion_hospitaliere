from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_validators_help_texts
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': _('Nom d’utilisateur'),
            'password1': _('Mot de passe'),
            'password2': _('Confirmation du mot de passe'),
        }
        help_texts = {
            'username': _('Choisis un nom d’utilisateur unique.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password_help = password_validators_help_texts()
        if password_help:
            help_text = '<ul>' + ''.join(f'<li>{text}</li>' for text in password_help) + '</ul>'
        else:
            help_text = _('Le mot de passe doit contenir au moins 8 caractères et ne doit pas être trop courant ou entièrement numérique.')
        self.fields['password1'].help_text = mark_safe(help_text)
        self.fields['password2'].help_text = _('Saisis à nouveau le même mot de passe pour confirmation.')
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input-field'})
