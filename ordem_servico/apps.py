from django.apps import AppConfig


class OrdemServicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ordem_servico'

    def ready(self):
        pass
