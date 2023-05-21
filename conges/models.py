from django.db import models
from employe.models import Employe


# Create your models here.

class Typeconges(models.Model):

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

ETAT = [
    ('NEW', 'Nouveau'),
    ('ATT', 'Attente'),
    ('VAL', 'Validé'),
    ('REJ', 'Rejeté'),
]
class Conges(models.Model):
    employe = models.ForeignKey(Employe, related_name='conges', on_delete=models.SET_NULL, null=True, blank=True)
    typeconges = models.ForeignKey(Typeconges, related_name='conges', on_delete=models.SET_NULL, null=True, blank=True)

    description = models.CharField(max_length=255)
    etatconges = models.CharField(choices=ETAT, max_length=40, default='NEW')
    datedebut = models.DateTimeField(blank=True)
    datefin = models.DateTimeField(blank=True)

    soft_deleting = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.employe, self.typeconges)

    @property
    def Calculduree(self):
        datedebut = self.datedebut
        datefin = self.datefin

        duree = (datefin - datedebut).days

        annee, resjours = divmod(duree, 365)
        mois, jours = divmod(resjours, 30)

        duree_conges = f"{annee} Ans {mois} Mois {jours} Jours "
        return duree_conges