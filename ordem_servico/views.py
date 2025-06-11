from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdemServico, Cliente
from .forms import OrdemServicoForm
from django.contrib import messages
from django.http import JsonResponse

def buscar_clientes_ajax(request):
    termo = request.GET.get('q', '')
    clientes = Cliente.objects.filter(nome__icontains=termo)[:10]
    results = [
        {'id': cliente.id, 'text': f"{cliente.nome} - {cliente.cpf}"}
        for cliente in clientes
    ]
    return JsonResponse({'results': results})

def criar_cliente_ajax(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        cliente = Cliente.objects.create(nome=nome, cpf=cpf, telefone=telefone)
        return JsonResponse({'id': cliente.id, 'nome': cliente.nome})

def lista_ordens(request):
    ordens = OrdemServico.objects.all().order_by('-id')
    return render(request, 'ordem_servico/lista.html', {'ordens': ordens})

def criar_ordem(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ordem de serviço criada com sucesso.")
            return redirect('lista_ordens')
    else:
        form = OrdemServicoForm()
    return render(request, 'ordem_servico/form.html', {'form': form, 'titulo': 'Nova Ordem de Serviço'})

def editar_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, pk=ordem_id)
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST, instance=ordem)
        if form.is_valid():
            os = form.save(commit=False)
            os.atualizado_por = request.user
            os.save()
            return redirect('detalhar_ordem', ordem_id=ordem.id)
    else:
        form = OrdemServicoForm(instance=ordem)
    return render(request, 'ordem_servico/editar_ordem.html', {'form': form})

def detalhar_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, pk=ordem_id)
    vias = ["Cliente", "Empresa"]
    return render(request, 'ordem_servico/detalhe_ordem.html', {
        'ordem': ordem,
        'vias': vias,
    })
