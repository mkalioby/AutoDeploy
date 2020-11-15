from django import forms
import json
from . import models


class PluginsForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'form-control', 'size': 60}))
    settings = forms.CharField(label='Settings', widget=forms.Textarea(attrs={'class': 'form-control', 'rows':80, 'cols':20}))

    class Meta:
        fields = ("name", "settings")
