from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import Q
from datetime import datetime
from .models import OrdemServico, Cliente, Anexo
from .forms import OrdemServicoForm

def buscar_clientes_ajax(request):
    termo = request.GET.get('term', '')
    clientes = Cliente.objects.filter(nome__icontains=termo)[:10]
    results = [
        {'id': cliente.id, 'text': f"{cliente.nome}"}
        for cliente in clientes
    ]
    return JsonResponse({'results': results})

def criar_cliente_ajax(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')

        if Cliente.objects.filter(cpf=cpf).exists():
            return JsonResponse({'erro': 'Já existe um cliente com esse CPF.'}, status=400)

        try:
            cliente = Cliente.objects.create(nome=nome, cpf=cpf, telefone=telefone)
            return JsonResponse({
                'id': cliente.id,
                'nome': f"{cliente.nome}"
            })
        except IntegrityError:
            return JsonResponse({'erro': 'Erro ao salvar cliente.'}, status=400)

    return JsonResponse({'erro': 'Requisição inválida.'}, status=400)

def lista_ordens(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        ordens = OrdemServico.objects.all()

        cliente = request.GET.get("cliente")
        situacao = request.GET.get("situacao")
        data_inicial = request.GET.get("data_inicial")
        data_final = request.GET.get("data_final")

        if cliente:
            ordens = ordens.filter(
                Q(cliente__nome__icontains=cliente) | Q(cliente__cpf__icontains=cliente)
            )

        if situacao:
            ordens = ordens.filter(situacao=situacao)

        if data_inicial:
            ordens = ordens.filter(data_os__gte=data_inicial)

        if data_final:
            ordens = ordens.filter(data_os__lte=data_final)

        data = []
        for os in ordens:
            data.append({
                'id': os.id,
                'cliente': str(os.cliente),
                'cpf': os.cliente.cpf,
                'responsavel': str(os.responsavel),
                'situacao': os.get_situacao_display(),
                'situacao_raw': os.situacao,
                'data_os': os.data_os.strftime("%d/%m/%Y"),
                'previsao_entrega': os.previsao_entrega.strftime("%d/%m/%Y") if os.previsao_entrega else '',
                'url_detalhe': f"/ordens/{os.id}/",
                'url_editar': f"/ordens/{os.id}/editar/" if os.situacao != 'fechada' else ''
            })
        return JsonResponse({'ordens': data})

    ordens = OrdemServico.objects.all().order_by('-id')

    cliente = request.GET.get("cliente")
    situacao = request.GET.get("situacao")
    data_inicial = request.GET.get("data_inicial")
    data_final = request.GET.get("data_final")

    if cliente:
        ordens = ordens.filter(
            Q(cliente__nome__icontains=cliente) | Q(cliente__cpf__icontains=cliente)
        )

    if situacao:
        ordens = ordens.filter(situacao=situacao)

    if data_inicial:
        ordens = ordens.filter(data_os__gte=data_inicial)

    if data_final:
        ordens = ordens.filter(data_os__lte=data_final)

    total_ordens = ordens.count()
    em_analise = ordens.filter(situacao='analise').count()
    fechadas = ordens.filter(situacao='fechada').count()
    abertas = ordens.filter(situacao='aberta').count()

    context = {
        'ordens': ordens,
        'total_ordens': total_ordens,
        'em_analise': em_analise,
        'fechadas': fechadas,
        'abertas': abertas,
    }
    return render(request, 'ordem_servico/lista.html', context)

def criar_ordem(request):
    cliente_id = request.GET.get('cliente_id')
    initial = {'cliente': cliente_id} if cliente_id else None

    if request.method == 'POST':
        form = OrdemServicoForm(request.POST, request.FILES)
        if form.is_valid():
            ordem = form.save(commit=False)
            ordem.criado_por = request.user
            ordem.save()

            arquivos = request.FILES.getlist('anexos')
            for arquivo in arquivos:
                Anexo.objects.create(ordem_servico=ordem, arquivo=arquivo)

            messages.success(request, "Ordem de serviço criada com sucesso.")
            return redirect('lista_ordens')
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = OrdemServicoForm(initial=initial)

    return render(request, 'ordem_servico/form.html', {
        'form': form,
        'titulo': 'Nova Ordem de Serviço'
    })

def editar_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, pk=ordem_id)
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST, request.FILES, instance=ordem)
        if form.is_valid():
            ordem = form.save(commit=False)
            ordem.atualizado_por = request.user
            ordem.save()

            arquivos = request.FILES.getlist('anexos')
            for arquivo in arquivos:
                Anexo.objects.create(ordem_servico=ordem, arquivo=arquivo)

            messages.success(request, "Ordem de serviço atualizada com sucesso.")
            return redirect('detalhar_ordem', ordem_id=ordem.id)
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = OrdemServicoForm(instance=ordem)

    return render(request, 'ordem_servico/editar_ordem.html', {
        'form': form,
        'titulo': f"Editar Ordem #{ordem.id}",
        'ordem': ordem
    })

def detalhar_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, pk=ordem_id)
    anexos = ordem.anexos.all()
    vias = ["Cliente", "Empresa"]

    return render(request, 'ordem_servico/detalhe_ordem.html', {
        'ordem': ordem,
        'vias': vias,
        'anexos': anexos
    })
