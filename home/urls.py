
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from home.views import dashboard, login_user, home_page,entry
from mysite import settings



urlpatterns = [

    path('', home_page, name='home'),

    path('login', login_user, name='login'),

    path('dashboard', dashboard, name='dashboard'),

    path('entree', entry, name='entry'),

]
