
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home.views import dashboard, login_user, pointage_page, entry, sortie, logout_view

from mysite import settings



urlpatterns = [

    path('', pointage_page, name='home'),

    path('login', login_user, name='login'),
    path('logout', logout_view, name='logout'),

    path('dashboard', dashboard, name='dashboard'),

    path('entree', entry, name='entry'),
    path('sortie', sortie, name='exit_'),

]
