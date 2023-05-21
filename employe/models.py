from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

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
    def create_user(self,first_name,last_name,email,password=None):
        if not email:
            raise ValueError("l'utilisateur doit avoir une adresse email")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,first_name,last_name,email,password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

USER_CHOICES = [
    ('E', 'Employe'),
    ('R', 'Rh'),
    ('AD','Admin')
]
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    #username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    user_type = models.CharField(choices=USER_CHOICES, max_length=5,default='E')

    # required
    soft_deleting = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = MyAccountManager()

    def _str_(self):
        return "{} {}".format(self.first_name, self.last_name)

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True

    @property
    def is_employe(self):
        if self.user_type == 'E':
            return True
        else:
            return False
    @property
    def is_Rh(self):
        if self.user_type == 'R':
            return True
        else:
            return False

GENDER_CHOICES = [
    ('H', 'Homme'),
    ('F', 'Femme'),
]
STATUT_MAT = [
    ('C', 'Célibataire'),
    ('M', 'Marié'),
]

class Employe(models.Model):
    account = models.OneToOneField(Account, related_name='employe', on_delete=models.SET_NULL, null=True, blank=True)
    departement = models.ForeignKey(Departement, related_name='employe', on_delete=models.SET_NULL, null=True, blank=True)
    lieuemploie = models.ForeignKey(LieuEmploi, related_name='employe', on_delete=models.SET_NULL, null=True, blank=True)
    poste = models.ForeignKey(Poste, related_name='employe', on_delete=models.SET_NULL, null=True, blank=True)

    faceid = models.IntegerField()

    name = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    genre = models.CharField(choices=GENDER_CHOICES, max_length=5)
    datenaiss = models.DateField()
    phone1 = models.CharField(max_length=100)
    phone2 = models.CharField(max_length=100)
    emailemp = models.CharField(max_length=255) #Email employe
    adress = models.CharField(max_length=255)
    numbank = models.CharField(max_length=255)
    nationnalite = models.CharField(max_length=255)
    statutmat = models.CharField(choices=STATUT_MAT, max_length=50)
    nbrechild = models.IntegerField()
    contacturgence = models.CharField(max_length=100)

    soft_deleting = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    def listcontrats(self):
        contrats = self.contrat.filter(soft_deleting=False).count()

        return contrats