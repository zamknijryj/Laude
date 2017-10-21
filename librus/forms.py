from django import forms
from .models import Oceny

class LibrusForm(forms.ModelForm):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Oceny
        exclude = ('oceny', 'test')
