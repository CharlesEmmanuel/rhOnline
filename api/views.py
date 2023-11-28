from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from api.serializers import TypecongesApi, CongesApi, ContratApi, PointageApi, PresenceApi, SinistreApi, DepartementApi, PosteApi, LieuEmploiApi, EmployeApi, AccountApi
from employe.models import Departement, Poste, LieuEmploi, Employe, Account
from conges.models import Conges, Typeconges
from contrat.models import Contrat
from presence.models import Pointage, Presence
from sinistre.models import Sinistre

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Type Congés Api Part
class TypecongesList(generics.ListAPIView ):
    queryset = Typeconges.objects.all()
    serializer_class = TypecongesApi
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class CreateTypeconges(generics.ListCreateAPIView):
    queryset = Typeconges.objects.all()
    serializer_class = TypecongesApi
class UpdateTypeconges(generics.UpdateAPIView):
    queryset = Typeconges.objects.all()
    serializer_class = TypecongesApi
class GetTypeconges(generics.RetrieveAPIView):
    queryset = Typeconges.objects.all()
    serializer_class = TypecongesApi
class DeleteTypeconges(generics.DestroyAPIView):
    queryset = Typeconges.objects.all()
    serializer_class = TypecongesApi


# Account Api Part
class CreateUser(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountApi, EmployeApi