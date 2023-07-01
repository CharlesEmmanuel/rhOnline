from django.db import models
from employe.models import Employe
from datetime import datetime, timedelta

# Create your models here.

CONTRAT = [
    ('STG', 'Stage'),
    ('CDD', 'Contrat à durée déterminé'),
    ('CDI', 'Contrat à durée indéterminé'),
]


class Contrat(models.Model):
    employe = models.ForeignKey(Employe, related_name='contrat', on_delete=models.SET_NULL, null=True, blank=True)

    typecontrat = models.CharField(choices=CONTRAT, max_length=40)
    mission = models.CharField(max_length=255)
    # statut = models.CharField(max_length=255)

    datedebut = models.DateField()
    datefin = models.DateField()

    salaire = models.CharField(max_length=255)

    soft_deleting = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.employe, self.typecontrat)

    @property
    def Calculduree(self):
        if self.typecontrat == 'CDI':
            duree_contrat = 'Indéterminé'
        else:
            datedebut = self.datedebut
            datefin = self.datefin

            duree = (datefin - datedebut).days

            annee, resjours = divmod(duree, 365)
            mois, jours = divmod(resjours, 30)

            duree_contrat = f"{annee} Ans {mois} Mois {jours} Jours "
        return duree_contrat

    def getContratType(self):
        if self.typecontrat == 'STG':
            return 'Stage'
        elif self.typecontrat == 'CDD':
            return 'Contrat à durée déterminée'
        elif self.typecontrat == 'CDI':
            return 'Contrat à durée indéterminée'
