from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import OrdemServico, OrdemServicoLog


@receiver(pre_save, sender=OrdemServico)
def log_alteracoes_ordem_servico(sender, instance, **kwargs):
    if not instance.pk:
        return  # Não loga criação

    try:
        old_instance = OrdemServico.objects.get(pk=instance.pk)
    except OrdemServico.DoesNotExist:
        return

    campos_para_log = ['descricao', 'data_recebimento', 'previsao_entrega',
                       'canal_venda', 'situacao', 'responsavel', 'cliente_id']

    for campo in campos_para_log:
        valor_antigo = getattr(old_instance, campo)
        valor_novo = getattr(instance, campo)
        if valor_antigo != valor_novo:
            OrdemServicoLog.objects.create(
                ordem_servico=instance,
                campo_modificado=campo,
                valor_antigo=str(valor_antigo),
                valor_novo=str(valor_novo),
                usuario=getattr(instance, '_usuario', None)  # Opcional
            )
