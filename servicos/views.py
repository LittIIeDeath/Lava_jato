from django.shortcuts import render, get_object_or_404
from .forms import FormServico
from django.http import HttpResponse, FileResponse
from .models import Servico
from fpdf import FPDF
from io import BytesIO

def novo_servico(request):
    if request.method == 'GET':
        form = FormServico()
        return render(request, 'novo_servico.html', {'form': form})
    elif request.method == 'POST':
        form = FormServico(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('dados salvos com sucesso')
        else:
            return render(request, 'novo_servico.html', {'form': form})

def listar_servico(request):
    if request.method == 'GET':
        servicos = Servico.objects.all()
        return render(request, 'listar_servico.html', {'servicos': servicos})

def servico(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)
    return render(request, 'servico.html', {'servico': servico})

def gerar_os(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 10)

    pdf.set_fill_color(240, 240, 240)
    pdf.cell(45, 10, 'Cliente:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.cliente.nome}', 1, 1, 'L', 1)

    pdf.cell(45, 10, 'Manuntençoes:', 1, 0, 'L', 1)

    categoria_manuntençao = servico.categoria_manuntencao.all()
    for i, manuntencao in enumerate(categoria_manuntençao):
        pdf.cell(0, 10, f'- {manuntencao.get_titulo_display()}', 1, 1, 'L', 1)
        if not i == len(categoria_manuntençao) -1:
            pdf.cell(45, 10, '', 1, 0, 'L', 1)
    
    pdf.cell(45, 10, 'Data de inicio:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.data_inicio}', 1, 1, 'L', 1)
    pdf.cell(45, 10, 'Data de entrega:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.data_entrega}', 1, 1, 'L', 1)
    pdf.cell(45, 10, 'Protocolo:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.protocolo}', 1, 1, 'L', 1)
    pdf.cell(45, 10, 'Preco total:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.preco_total()}', 1, 1, 'L', 1)

    pdf_content = pdf.output(dest='S').encode('latin1')
    pdf_bytes = BytesIO(pdf_content)
    return FileResponse(pdf_bytes, as_attachment=True, filename=f'os-{servico.protocolo}.pdf')