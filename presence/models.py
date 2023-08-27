from django.db import models
from employe.models import Employe
import datetime

# Create your models here.
class Presence(models.Model):
    employe = models.ForeignKey(Employe, related_name='presence', on_delete=models.SET_NULL, null=True, blank=True)
    observation = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)
    datedebut = models.DateTimeField(blank=True,null=True)
    datefin = models.DateTimeField(null=True, blank=True)
    state = models.BooleanField(default=False)
    # temptravail = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.employe, self.temptravail)

    @property
    def calcultime(self):
        if self.datedebut and self.datefin:
            temps_travail = self.datefin - self.datedebut
            heures = temps_travail.seconds // 3600
            minutes = (temps_travail.seconds // 60) % 60
            secondes = temps_travail.seconds % 60
            return f"{heures:02d}h : {minutes:02d}min : {secondes:02d}sec"
        return "----"



class Pointage(models.Model):
    employee = models.ForeignKey(Employe,related_name='pointages', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    date_time = models.DateTimeField(null=True, blank=True)
    present = models.BooleanField(default=False)
    is_out = models.BooleanField(default=False)