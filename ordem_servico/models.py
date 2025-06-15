from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"


class Funcionario(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Situacao(models.TextChoices):
    ABERTA = 'aberta', 'Aberta'
    ANALISE = 'analise', 'Em Análise'
    FECHADA = 'fechada', 'Fechada'


class CanalVenda(models.TextChoices):
    PRESENCIAL = 'presencial', 'Presencial'
    ONLINE = 'online', 'Online'


class OrdemServico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    responsavel = models.ForeignKey(Funcionario, on_delete=models.PROTECT)
    situacao = models.CharField(
        max_length=10,
        choices=Situacao.choices,
        default=Situacao.ABERTA
    )
    data_os = models.DateField()
    previsao_entrega = models.DateField()
    canal_venda = models.CharField(
        max_length=10,
        choices=CanalVenda.choices,
        default=CanalVenda.PRESENCIAL
    )

    equipamento = models.CharField(max_length=100)
    marca = models.CharField(max_length=50, blank=True)
    modelo = models.CharField(max_length=50, blank=True)
    serie = models.CharField(max_length=50, blank=True)

    condicoes = models.TextField(blank=True)
    defeitos = models.TextField(blank=True)
    acessorios = models.TextField(blank=True)
    solucao = models.TextField(blank=True)
    laudo_tecnico = models.TextField(blank=True)
    termos_garantia = models.TextField(blank=True)

    def __str__(self):
        return f"OS #{self.id} - {self.cliente.nome} - {self.situacao}"

    def clean(self):
        if self.previsao_entrega < self.data_os:
            raise ValidationError({
                'previsao_entrega': _('A data de entrega não pode ser anterior à data de abertura da OS.')
            })

    def salvar_status(self):
        if self.pk:
            old = OrdemServico.objects.get(pk=self.pk)
            if old.situacao == Situacao.FECHADA and self.situacao != Situacao.FECHADA:
                raise ValueError("OS fechada não pode ser reaberta.")
        self.save()


class Anexo(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, related_name='anexos', on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='anexos/')
    descricao = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.arquivo.name
