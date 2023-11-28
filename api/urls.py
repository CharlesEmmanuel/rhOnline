from django.urls import path

from api.views import TypecongesList, CreateTypeconges, UpdateTypeconges, GetTypeconges, DeleteTypeconges, CreateUser

urlpatterns = [
    path('typeconges/', TypecongesList.as_view(), name='typecongeslistapi'),
    path('createtypeconges/', CreateTypeconges.as_view(), name='createtypecongesapi'),
    path('updatetypeconges/<int:pk>', UpdateTypeconges.as_view(), name='updatetypeconges'),
    path('gettypeconges/<int:pk>', GetTypeconges.as_view(), name='gettypeconges'),

    path('deltypeconges/<int:pk>', DeleteTypeconges.as_view(), name='deltypeconges'),

    path('createuser/', CreateUser.as_view(), name='createuser'),

]
