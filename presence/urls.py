from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from presence.views import checkin_face,checkout_face,liste_presence

urlpatterns = [
    # PRESENCE POINTAGE
    path('', liste_presence, name='liste_presence'),
    path('checkin/', checkin_face, name='check_in'),
    path('checkout/', checkout_face, name='check_out'),


]
