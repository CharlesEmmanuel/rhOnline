
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from home.views import dashboard, login_user, pointage_page
=======
from home.views import dashboard, login_user, home_page,entry
>>>>>>> 68304463259f30b7e2cd203ff40043a03920acd2
from mysite import settings



urlpatterns = [

    path('', pointage_page, name='home'),

    path('login', login_user, name='login'),

    path('dashboard', dashboard, name='dashboard'),

    path('entree', entry, name='entry'),

]
