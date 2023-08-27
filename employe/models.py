from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.safestring import mark_safe
import os


# Create your models here.

class Departement(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    soft_deleting = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Poste(models.Model):
    name = models.CharField(max_length=255)
    mission = models.CharField(max_length=255)
    soft_deleting = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LieuEmploi(models.Model):
    name = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    soft_deleting = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, user_type, password=None):
        if not email:
            raise ValueError("l'utilisateur doit avoir une adresse email")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_type='AD',
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def autoCreateEmploye(self):
        pass

    def autoCreateDepartment(self, nom, description):

        pass

    def autoCreatePoste(self, nom, mission):
        pass

    def autoCreateLiEmploi(self, nom, adresse):
        pass


USER_CHOICES = [
    ('E', 'Employe'),
    ('R', 'Ressources Humaines'),
    ('AD', 'Administrateur')
]


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    user_type = models.CharField(choices=USER_CHOICES, max_length=5, default='E')

    # required
    soft_deleting = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def _str_(self):
        return "{} {}".format(self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    @property
    def is_employe(self):
        if self.user_type == 'E':
            return 'EMPLOYÉ'
        else:
            return False

    @property
    def is_Rh(self):
        if self.user_type == 'R':
            return 'RESSOURCES HUMAINES'
        else:
            return False

    def statutemp(self):
        if (self.user_type == 'E'):
            return 'EMPLOYÉ'
        elif (self.user_type == 'R'):
            return 'RESSOURCES HUMAINES'
        elif (self.user_type == 'AD'):
            return 'ADMINISTRATEUR'


GENDER_CHOICES = [
    ('H', 'Homme'),
    ('F', 'Femme'),
]
STATUT_MAT = [
    ('C', 'Célibataire'),
    ('M', 'Marié'),
]


def renameImage(instance, filename):
    upload_to = 'employe'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Employe(models.Model):
    account = models.OneToOneField(Account, related_name='employe', on_delete=models.SET_NULL, null=True, blank=True)
    departement = models.ForeignKey(Departement, related_name='employe', on_delete=models.SET_NULL, null=True,
                                    blank=True)
    lieuemploie = models.ForeignKey(LieuEmploi, related_name='employe', on_delete=models.SET_NULL, null=True,
                                    blank=True)
    poste = models.ForeignKey(Poste, related_name='employe', on_delete=models.SET_NULL, null=True, blank=True)

    faceid = models.IntegerField()

    name = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    genre = models.CharField(choices=GENDER_CHOICES, max_length=5)
    datenaiss = models.DateField()
    phone1 = models.CharField(max_length=100)
    phone2 = models.CharField(max_length=100)
    emailemp = models.CharField(max_length=255)  # Email employe
    adress = models.CharField(max_length=255)
    numbank = models.CharField(max_length=255)
    statutmat = models.CharField(choices=STATUT_MAT, max_length=50)
    nbrechild = models.IntegerField()
    contacturgence = models.CharField(max_length=100)
    photoemp = models.ImageField(blank=True, upload_to=renameImage, null=True, default="employe/photo_default-1.jpg")

    soft_deleting = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " " + self.prenom

    def listcontrats(self):
        contrats = self.contrat.filter(soft_deleting=False).count()
        return contrats

    def getGenre(self):
        if (self.genre == 'H'):
            return 'Homme'
        else:
            return 'Femme'

    def getStatutMat(self):
        if (self.statutmat == 'C'):
            return 'CÉLIBATAIRE'
        else:
            return 'MARIÉ'

    def imageEmp(self):
        return mark_safe('<img src="{}"  height="20">').format(self.photoemp.url)
