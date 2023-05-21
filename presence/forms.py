
from django import forms
from django.contrib.gis import forms

from django.forms import TextInput, EmailInput, Select, FileInput, DateInput, DateTimeInput, SelectDateWidget,Textarea
from floppyforms.gis import PointWidget


import folium

from rhOnline.employe.models import Employe

CITY_CHOICES = (
    ('Abidjan', 'Abidjan'),
    ('Yamoussoukro', 'Yamoussoukro'),
    ('Bouake', 'Bouake'),
    ('Korogo', 'Korogo'),
    ('Man', 'Man'),
    ('Abengourou', 'Abengourou'),
    ('San-Pedro', 'San Pedro'),
    ('Bassam', 'Bassam'),
    ('Dabou', 'Dabou'),
    ('Agboville', 'Agboville'),
)
m = folium.Map(width=800,height=500,location=[43.61092, 3.87723])
m = m._repr_html_()



EMPLOYEE_CHOICES = Employe.objects.all().values_list('name','name')
class UsernameAndDateForm(forms.Form):
    username = forms.CharField(widget=forms.Select(attrs={'placeholder': 'Employee'},choices=EMPLOYEE_CHOICES))
    date_from=forms.DateField(widget = forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day",)))
    date_to=forms.DateField(widget = forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))



class DateForm(forms.Form):
	date=forms.DateField(widget = forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))

class DateForm_2(forms.Form):
	date_from=forms.DateField(widget = forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
	date_to=forms.DateField(widget = forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))


