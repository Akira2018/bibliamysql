from django.apps import AppConfig
from django.db import models

class GestaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestao'

    def ready(self):
        from . import signals  # Importe seus signals aqui

        # Certifique-se de que os modelos estão carregados
        from .models import (EntradaFinanceira, SaidaFinanceira, BalanceteMensal, SaldoAnual,
                             BancoFinanceiro, MovimentoFinanceiro, MembroFinanceiro, Agendapastoral,
                             Agendaigreja, Cadastroestudos, Batismoigreja, CadastroContas, CadastroSubcontas,
                             ContasPagar, Biblioteca, Profissao, Patrimonio, Fornecedor, Habilidades, EmprestimoLivro)


