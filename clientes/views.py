from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Carro
import re
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

# Create your views here.
def clientes(request):
    if request.method == 'GET':
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        # verificador de usuario ja cadastrado
        cliente = Cliente.objects.filter(cpf=cpf)
        if cliente.exists():
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'carros': zip(carros, placas, anos)})
        
        # verificador de email invalidado
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros, placas, anos)})

        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )
        cliente.save()

        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(
                carro = carro,
                placa = placa,
                ano = ano,
                cliente = cliente
            )
            car.save()
            
        return HttpResponse("cadastrado com sucesso")

def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    carros = Carro.objects.filter(cliente=cliente[0])
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']

    carros_json = json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': carro['fields'], 'id': carro['pk']} for carro in carros_json]
    data = {'cliente': cliente_json, 'carros': carros_json, 'cliente_id': cliente_id}
    return JsonResponse(data)

@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get('carro')
    placa = request.POST.get('placa')
    ano = request.POST.get('ano')
    
    carro = Carro.objects.get(id=id)
    list_carros = Carro.objects.filter(placa=placa).exclude(id=id)
    if list_carros.exists():
        return HttpResponse('Placa ja existe')

    carro.carro = nome_carro
    carro.placa = placa
    carro.ano = ano
    carro.save()
    return HttpResponse('cadastrado')

def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}')
    except:
        #TO-DO: exibir msg de erro
        return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}')

def update_cliente(request, id):
    body = json.loads(request.body)
    
    nome = body['nome']
    sobrenome = body['sobrenome']
    cpf = body['cpf']
    email = body['email']

    cliente = get_object_or_404(Cliente, id=id)

    # verificador de cpf ja cadastrado
    cpf_list = Cliente.objects.filter(cpf=cpf).exclude(id=id)
    email_list = Cliente.objects.filter(email=email).exclude(id=id)
    if cpf_list.exists():
        return JsonResponse({'status': '201'})
    elif email_list.exists():
        return JsonResponse({'status': '202'})
    else:
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return JsonResponse({'status': '203'})
        try:
            cliente.nome = nome
            cliente.sobrenome = sobrenome
            cliente.cpf = cpf
            cliente.email = email
            cliente.save()
            return JsonResponse({'status': '200', 'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf})
        except:
            return JsonResponse({'status': '500'})