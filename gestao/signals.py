from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from decimal import Decimal
from .models import EntradaFinanceira, SaidaFinanceira, BalanceteMensal, SaldoAnual

def atualizar_balancete_mensal_e_saldo_anual(instance):
    # Obter o ano e o mês da entrada financeira
    if isinstance(instance, EntradaFinanceira):
        mes = instance.data_entrada.month
        ano = instance.data_entrada.year
    elif isinstance(instance, SaidaFinanceira):
        mes = instance.data_saida.month
        ano = instance.data_saida.year
    else:
        return

    # Atualizar o balancete mensal
    balancete, created = BalanceteMensal.objects.get_or_create(mes=mes, ano=ano)
    total_entradas = EntradaFinanceira.objects.filter(data_entrada__year=ano, data_entrada__month=mes).aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
    total_saidas = SaidaFinanceira.objects.filter(data_saida__year=ano, data_saida__month=mes).aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
    balancete.total_entradas = total_entradas
    balancete.total_saidas = total_saidas
    balancete.saldo_mensal = total_entradas - total_saidas
    balancete.save()

    # Atualizar o saldo anual
    saldo_anual, created = SaldoAnual.objects.get_or_create(ano=ano)
    total_entradas_ano = EntradaFinanceira.objects.filter(data_entrada__year=ano).aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
    total_saidas_ano = SaidaFinanceira.objects.filter(data_saida__year=ano).aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
    saldo_anual.total_entradas_ano = total_entradas_ano
    saldo_anual.total_saidas_ano = total_saidas_ano
    saldo_anual.saldo_anual = total_entradas_ano - total_saidas_ano
    saldo_anual.save()

@receiver(post_save, sender=EntradaFinanceira)
@receiver(post_save, sender=SaidaFinanceira)
@receiver(post_delete, sender=EntradaFinanceira)
@receiver(post_delete, sender=SaidaFinanceira)
def atualizar_balancetes(sender, instance, **kwargs):
    atualizar_balancete_mensal_e_saldo_anual(instance)
