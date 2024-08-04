from django.apps import AppConfig

class GestaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestao'

    def ready(self):
        import gestao.signals  # Certifique-se de que o módulo signals está importado





