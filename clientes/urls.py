from django.urls import path
from . import views

urlpatterns = [
    path('', views.Clientes, name="Clientes")
]
