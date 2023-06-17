from django.db import models

from employe.models import Employe


# Create your models here.
class Sinistre(models.Model):
    employe = models.ForeignKey(Employe, related_name='sinistre', on_delete=models.SET_NULL, null=True, blank=True)

    description = models.CharField(max_length=255)
    datesinistre = models.DateTimeField(blank=True)
    soft_deleting = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.employe, self.datesinistre)