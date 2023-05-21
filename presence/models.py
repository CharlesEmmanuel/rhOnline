from django.db import models
from employe.models import Employe


# Create your models here.
class Presence(models.Model):
    employe = models.ForeignKey(Employe, related_name='presence', on_delete=models.SET_NULL, null=True, blank=True)

    observation = models.CharField(max_length=255)
    datedebut = models.DateTimeField(blank=True)
    datefin = models.DateTimeField(blank=True)
    temptravail = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.employe, self.temptravail)