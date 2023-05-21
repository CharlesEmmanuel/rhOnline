from django import forms
from django.forms import TextInput, ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

from conges.models import Typeconges


class TypecongesForm(ModelForm):
    class Meta:
        model = Typeconges
        fields = ['name', 'description']
        labels = {
            'name': _('Nom'),
            'description': _('description')
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez saisir le nom du type de congé', 'required': 'required'}),
            'description': Textarea(attrs={'class': 'form-control', 'required': 'required', 'style': 'height:250px;'}),
        }
