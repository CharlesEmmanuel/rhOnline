from django import forms
from django.forms import TextInput, EmailInput, Select, FileInput, ModelForm, Textarea,NumberInput
from django.utils.translation import gettext_lazy as _
from employe.models import Departement, Poste, LieuEmploi, Employe


class DateInput(forms.DateInput):
    input_type = "date"


class DepartementForm(ModelForm):
    class Meta:
        model = Departement
        fields = ['name', 'description']
        labels = {
            'name': _('Nom'),
            'description': _('Description')
        }
        error_messages = {
            'name': {
                'max_length' : _("Error: maximum length limit is 255 characters"),
            }
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder' : 'Veuillez saisir le nom du departement' , 'required': 'required'}),
            'description': Textarea(attrs={'class': 'form-control', 'required': 'required'}),
        }


class PosteForm(ModelForm):
    class Meta:
        model = Poste
        fields = ['name', 'mission']
        labels = {
            'name' : _('Nom'),
            'mission' : _('Mission')
        }
        widgets = {
            'name': Textarea(attrs={'class': 'form-control', 'placeholder' : 'Veuillez saisir le nom du poste', 'required' : 'required' }),
            'mission': Textarea(attrs={'class': 'form-control','required' : 'required'}),
        }

class LiemploiForm(ModelForm):
    class Meta:
        model = LieuEmploi
        fields = ['name', 'adresse']
        labels = {
            'name' : _('Nom'),
            'adresse' : _('adresse')
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder' : 'Veuillez saisir le nom du Lieu d\'emploi' , 'required': 'required'}),
            'adresse': Textarea(attrs={'class': 'form-control', 'required': 'required'}),
        }

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['account', 'departement', 'lieuemploie', 'poste', 'name', 'prenom', 'genre', 'datenaiss', 'phone1', 'phone2', 'adress', 'numbank', 'statutmat', 'nbrechild', 'contacturgence']
        labels = {
            'account': _('Compte'),
            'departement': _('Département'),
            'lieuemploie': _('Lieu D\'emploie'),
            'poste': _('Poste'),
            'name': _('Nom'),
            'prenom': _('Prénom'),
            'genre': _('Genre'),
            'datenaiss': _('Date de Naissance'),
            'phone1': _('Téléphone 1'),
            'phone2': _('Téléphone 2'),
            'adress': _('Adresse'),
            'numbank': _('Numero Bancaire'),
            'statutmat': _('Statut Matrimonial'),
            'nbrechild': _('Nombre d\'enfants'),
            'contacturgence': _('Contact d\'urgence'),
        }
        widgets = {
            'account': forms.Select(attrs={'name': 'new_name_account', 'class': 'form-control', 'required': 'required'}),
            'departement': forms.Select(attrs={'name': 'new_name_departement', 'class': 'form-control', 'required': 'required'}),
            'lieuemploie': forms.Select(attrs={'name': 'new_name_lieuemploie', 'class': 'form-control', 'required': 'required'}),
            'poste': forms.Select(attrs={'name': 'new_name_poste', 'class': 'form-control', 'required': 'required'}),

            'name': forms.TextInput(attrs={'name': 'new_name_name', 'class': 'form-control', 'required': 'required'}),
            'prenom': forms.TextInput(attrs={'name': 'new_name_prenom', 'class': 'form-control', 'required': 'required'}),
            'genre': forms.Select(attrs={'name': 'new_name_genre', 'class': 'form-control', 'required': 'required'}),
            'datenaiss': forms.DateInput(attrs={'name': 'new_name_datenaiss', 'class': 'form-control', 'required': 'required'}),
            'phone1': forms.TextInput(attrs={'name': 'new_name_phone1', 'class': 'form-control', 'required': 'required'}),
            'phone2': forms.TextInput(attrs={'name': 'new_name_phone2', 'class': 'form-control', 'required': 'required'}),
            'adress': forms.TextInput(attrs={'name': 'new_name_adress', 'class': 'form-control', 'required': 'required'}),
            'numbank': forms.TextInput(attrs={'name': 'new_name_numbank', 'class': 'form-control', 'required': 'required'}),
            'statutmat': forms.Select(attrs={'name': 'new_name_statutmat', 'class': 'form-control', 'required': 'required'}),
            'nbrechild': forms.NumberInput(attrs={'name': 'new_name_nbrechild', 'class': 'form-control', 'required': 'required'}),
            'contacturgence': forms.TextInput(attrs={'name': 'new_name_contacturgence', 'class': 'form-control', 'required': 'required'}),
        }

