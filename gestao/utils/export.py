from django.http import HttpResponse
from openpyxl import Workbook

from gestao.models import BalanceteMensal


def export_balancete_mensal(request):
    balancetes = BalanceteMensal.objects.all()

    # Criar um novo workbook do Excel
    wb = Workbook()
    ws = wb.active

    # Adicionar cabeçalho
    ws.append(['Mês', 'Ano', 'Total de Entradas', 'Total de Saídas', 'Saldo Mensal'])

    # Adicionar dados
    for balancete in balancetes:
        ws.append([
            balancete.nome_mes(),
            balancete.ano,
            balancete.total_entradas,
            balancete.total_saidas,
            balancete.saldo_mensal
        ])

    # Salvar o workbook em um objeto de HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=balancete_mensal.xlsx'
    wb.save(response)

    return response
