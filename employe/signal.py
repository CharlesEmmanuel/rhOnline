from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from employe.models import Departement, Poste, LieuEmploi, Account, Employe

class EmployeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employe'

    def ready(self):
        from employe.signal import create_initial_records

        post_migrate.connect(create_initial_records, sender=self)
@receiver(post_migrate)
def create_initial_records(sender, **kwargs):
    if sender.name == 'employe':
        # Create instances of your models here
        # For example:
        departement = Departement.objects.get_or_create(name='Departement 1', description='Description ')[0]
        poste = Poste.objects.get_or_create(name='Poste 1', mission='Mission 1')[0]
        lieuemploi = LieuEmploi.objects.get_or_create(name='Lieu Emploi 1', adresse='Adresse 1')[0]

        # Create an instance of Account with user_type 'AD'
        admin_account = Account.objects.get_or_create(
            email='admin@gmail.com',
            first_name='John',
            last_name='Doe',
            user_type='AD'
        )[0]
        admin_account.set_password('adminpassword')  # Set the desired password
        admin_account.save()

        # Create an instance of Employe
        admin_employe = Employe.objects.get_or_create(
            account=admin_account,
            departement=departement,
            lieuemploie=lieuemploi,
            poste=poste,
            faceid=admin_account.pk,  # Set the desired face ID
            name='John',
            prenom='Doe',
            genre='H',
            datenaiss='2000-01-01',  # Set the desired date of birth
            phone1='1234567890',  # Set the desired phone number
            emailemp='admin@gmail.com',
            adress='Admin Address',
            numbank='123456789',  # Set the desired bank number
            statutmat='C',
            nbrechild=0,
            contacturgence='15152505025',
        )[0]

        # Display a message indicating that records are being created
        print("Initial records created for your_app_name")

        # You can also create other instances of Account and Employe if needed
