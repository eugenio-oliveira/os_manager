from django.contrib import admin
from .models import Cliente, Funcionario, OrdemServico

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf')
    search_fields = ('nome', 'cpf')


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'responsavel', 'situacao', 'data_os', 'previsao_entrega')
    list_filter = ('situacao', 'canal_venda')
    search_fields = ('cliente__nome', 'cliente__cpf')
    readonly_fields = ('situacao',)

    def get_readonly_fields(self, request, obj=None):
        # Só permite edição de status se ainda não estiver "fechada"
        if obj and obj.situacao == 'fechada':
            return self.readonly_fields + (
                'cliente', 'responsavel', 'data_os', 'previsao_entrega',
                'canal_venda', 'equipamento', 'marca', 'modelo', 'serie',
                'condicoes', 'defeitos', 'acessorios', 'solucao',
                'laudo_tecnico', 'termos_garantia'
            )
        return self.readonly_fields
