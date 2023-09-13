from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def Clientes(request):
    return HttpResponse("pagina clientes")