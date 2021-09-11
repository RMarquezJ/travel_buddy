from django.urls import path
from . import views

urlpatterns = [
  path('', views.register),
  path('login', views.login),
  path('travels', views.mainpage),
  path('logout', views.logout),
  path('addtrip', views.addtrip),
  path('view/<tripid>', views.view),
  path('delete/<tripid>', views.delete),
  path('join/<tripid>', views.join),
  path('cancel/<tripid>', views.cancel),
]