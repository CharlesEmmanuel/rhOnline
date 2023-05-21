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
    temptravail = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.employe, self.temptravail)




class Pointage(models.Model):
    employee = models.ForeignKey(Employe,related_name='pointages', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    date_time = models.DateTimeField(null=True, blank=True)
    present = models.BooleanField(default=False)
    is_out = models.BooleanField(default=False)