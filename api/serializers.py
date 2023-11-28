from rest_framework import serializers
from rest_framework.authtoken.models import Token

from employe.models import Departement, Poste, LieuEmploi, Employe, Account
from conges.models import Conges, Typeconges
from contrat.models import Contrat
from presence.models import Pointage,Presence
from sinistre.models import Sinistre


class TypecongesApi(serializers.ModelSerializer):
    class Meta:
        model = Typeconges
        fields = '__all__'

class CongesApi(serializers.ModelSerializer):
    class Meta:
        model = Conges
        fields = '__all__'

class ContratApi(serializers.ModelSerializer):
    class Meta:
        model = Contrat
        fields = '__all__'


class PointageApi(serializers.ModelSerializer):
    class Meta:
        model = Pointage
        fields = '__all__'

class PresenceApi(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = '__all__'

class SinistreApi(serializers.ModelSerializer):
    class Meta:
        model = Sinistre
        fields = '__all__'


class DepartementApi(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = '__all__'

class PosteApi(serializers.ModelSerializer):
    class Meta:
        model = Poste
        fields = '__all__'

class LieuEmploiApi(serializers.ModelSerializer):
    class Meta:
        model = LieuEmploi
        fields = '__all__'

class EmployeApi(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = '__all__'

class AccountApi(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def create(self, validated_data):
        account = Account.objects.create_user(first_name=validated_data['first_name'], last_name=validated_data['last_name'], email=validated_data['email'], user_type=validated_data['user_type'], password= validated_data['password'])
        token_object, _ = Token.objects.get_or_create(user = account)
        return account
