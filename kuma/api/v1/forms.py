from django import forms
from django.conf import settings




class AccountSettingsForm(forms.Form):
    locale = forms.ChoiceField(required=False, choices=list(settings.LANGUAGES))
