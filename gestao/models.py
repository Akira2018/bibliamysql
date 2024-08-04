from django.dispatch import receiver
from django.db.models import Sum
from django.db.models import F, Q, functions as fn
from django.db.models.signals import post_save, post_delete
from django.core.validators import RegexValidator
import requests
from django.contrib import messages
from datetime import date
from django.utils.html import mark_safe
import logging
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.urls import reverse
logger = logging.getLogger(__name__)

class Biblia(models.Model):
    capitulo = models.IntegerField()
    versiculo = models.IntegerField()
    nome_livro = models.CharField(max_length=100)
    texto_biblico = models.TextField()
    tipo_testamento = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Bíblia Sagrada"
        verbose_name_plural = "Bíblia Sagrada"

    def __str__(self):
        return f"{self.nome_livro} - Capítulo {self.capitulo}, Versículo {self.versiculo}"
class Cadastroestudos(models.Model):
    titulo = models.TextField(verbose_name='Título do Estudo Bíblico:', help_text='Digite a descrição aqui: ')
    descricao = models.TextField(verbose_name='Descrição do Evento:', help_text='Digite a descrição aqui: ')
    data_registro = models.DateField(verbose_name='Data do Registro')

    class Meta:
        verbose_name = "Esboços Bíblicos"
        verbose_name_plural = "Esboços Bíblicos"

    def __str__(self):
        return self.titulo if self.titulo else 'Campo vazio'

class Agendapastoral(models.Model):
    descricao = models.TextField(verbose_name='Descrição do Evento:', help_text='Digite a descrição aqui: ')
    data_evento = models.DateField(verbose_name='Data do Evento')

    class Meta:
        verbose_name = "Agenda Pastoral"
        verbose_name_plural = "Agenda Pastoral"

    def __str__(self):
        return self.descricao if self.descricao else 'Campo vazio'

class Agendaigreja(models.Model):
    descricao = models.TextField(verbose_name='Descrição do Evento:', help_text='Digite a descrição aqui: ')
    data_evento = models.DateField(verbose_name='Data do Evento')

    class Meta:
        verbose_name = "Agenda da Igreja"
        verbose_name_plural = "Agenda da Igreja"

    def __str__(self):
        return self.descricao if self.descricao else 'Campo vazio'

class Batismoigreja(models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome do Batizando:', help_text='Digite o nome aqui: ')
    data_batismo = models.DateField(verbose_name='Data do Batismo')

    class Meta:
        verbose_name = "Cadastro de Batismo"
        verbose_name_plural = "Cadastro de Batismo"

    def __str__(self):
        return self.nome if self.nome else 'Campo vazio'

class Profissao(models.Model):
    nome_prof = models.CharField(max_length=80, unique=True, verbose_name='Nome da Profissão')

    def __str__(self):
        return self.nome_prof

    class Meta:
        verbose_name = 'Profissão'
        verbose_name_plural = 'Profissões'

class Habilidades(models.Model):
    nome_habilidade = models.CharField(max_length=80, unique=True, verbose_name='Nome da Habilidade')

    def __str__(self):
        return self.nome_habilidade

    class Meta:
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'

class MembroFinanceiro(models.Model):
    nome_membro = models.CharField(max_length=100, verbose_name='Nome do Membro')
    foto = models.ImageField(upload_to='fotos_membros/', verbose_name='Foto do Membro', null=True, blank=True)

    def foto_tag(self):
        if hasattr(self, 'foto') and self.foto:
            return mark_safe(f'<img src="{self.foto.url}" width="150" height="150" />')
        return "No Image"

    foto_tag.short_description = 'Foto'

    data_aniversario = models.DateField(verbose_name='Data de Nascimento', null=True, blank=True)
    estado_civil = models.CharField(
        max_length=20,
        choices=[
            ('Casado(a)', 'Casado(a)'),
            ('Solteiro(a)', 'Solteiro(a)'),
            ('Divorciado(a)', 'Divorciado(a)'),
            ('Viúvo(a)', 'Viúvo(a)'),
            ('Não informou', 'Não informou'),
        ],
        verbose_name='Estado Civil',
        null=True,
        blank=True,
        default='Não informou'
    )
    cargo = models.CharField(
        max_length=100,
        choices=[
            ('Membro(a)', 'Membro(a)'),
            ('Pastor(a)', 'Pastor(a)'),
            ('Pastor(a) Auxiliar', 'Pastor(a) Auxiliar'),
            ('Líder de grupo caseiro', 'Líder de grupo caseiro'),
            ('Diácono(nisa)', 'Diácono(nisa)'),
            ('Presbítero(a)', 'Presbítero(a)'),
            ('Bispo(a)', 'Bispo(a)'),
            ('Apostolo(a)', 'Apostolo(a)'),
            ('Padre', 'Padre'),
            ('Frei', 'Frei'),
            ('Sacerdote', 'Sacerdote'),
            ('Ancião', 'Ancião'),
            ('Visitante', 'Visitante'),
            ('Outros', 'Outros')
        ],
        verbose_name='Nome do Cargo',
        null=True,
        blank=True,
        default='Membro(a)'
    )
    grupo = models.CharField(
        max_length=100,
        choices=[
            ('Pastor Senior', 'Pastor Senior'),
            ('Pastor(a) Auxiliar', 'Pastor(a) Auxiliar'),
            ('Líder de grupo caseiro', 'Líder de grupo caseiro'),
            ('Líder de Ministério de Louvor', 'Líder de Ministério de Louvor'),
            ('Professor de Escola Dominical', 'Professor de Escola Dominical'),
            ('Líder de Ministério Infantil', 'Líder de Ministério Infantil'),
            ('Líder de Ministério das Mulheres', 'Líder de Ministério das Mulheres'),
            ('Líder de Ministério dos Jovens', 'Líder de Ministério dos Jovens'),
            ('Líder de Ministério das Crianças', 'Líder de Ministério das Crianças'),
            ('Líder de Organização de Festas', 'Líder de Organização de Festas'),
            ('Líder de Organização do Presépio', 'Líder de Organização do Presépio'),
            ('Líder de Organização Festa de Inverno', 'Líder de Organização Festa de Inverno'),
            ('Líder de Reunião de Oração', 'Líder de Reunião de Oração'),
            ('Líder de Circulo de Oração', 'Líder de Circulo de Oração'),
            ('Membro da Diretoria Administrativa', 'Membro da Diretoria Administrativa'),
            ('Membro do Conselho de Pastores', 'Membro do Conselho de Pastores'),
            ('Não ocupa cargo de Liderança', 'Não ocupa cargo de Liderança')
        ],
        verbose_name='Líder de Ministério',
        null=True,
        blank=True,
        default='Não ocupa cargo de Liderança'
    )

    nome_prof = models.ForeignKey(
        'Profissao',
        on_delete=models.CASCADE,
        verbose_name='Profissao',
        null=True,
        blank=True,
        default=None
    )
    nome_habilidade = models.ForeignKey(
        'Habilidades',
        on_delete=models.CASCADE,
        verbose_name='Habilidade',
        null=True,
        blank=True,
        default=None
    )

    email = models.EmailField(max_length=100, verbose_name='Email', blank=True)
    numero_telefone = models.CharField(max_length=15, verbose_name='Número de Telefone', blank=True)
    cpf = models.CharField(
        max_length=11,
        verbose_name='Número de CPF',
        blank=True,
        validators=[RegexValidator(regex=r'^\d{11}$', message='CPF deve ter 11 dígitos')]
    )
    rg = models.CharField(max_length=15, verbose_name='Número do RG', blank=True)
    cep = models.CharField(
        max_length=8,
        verbose_name='CEP do Imóvel:', blank=True,
        validators=[RegexValidator(regex=r'^\d{8}$', message='CEP deve ter 8 dígitos')]
    )
    logradouro = models.CharField(max_length=100, verbose_name='Nome da Rua:', blank=True)
    complemento = models.CharField(max_length=100, verbose_name='Complemento:', blank=True, null=True)
    bairro = models.CharField(max_length=50, verbose_name='Bairro:', blank=True)
    cidade = models.CharField(max_length=50, verbose_name='Cidade:', blank=True)
    uf = models.CharField(max_length=2, verbose_name='Estado:', blank=True)
    nr_imovel = models.CharField(max_length=10, verbose_name='Número do Imóvel', blank=True)
    observacao = models.TextField(max_length=100, blank=True, verbose_name='Observação: ')

    SITUACAO_CHOICES = [
        ('Ativo(a)', 'Ativo(a)'),
        ('Desligado(a)', 'Desligado(a)'),
    ]
    situacao = models.CharField(
        max_length=15,
        choices=SITUACAO_CHOICES,
        verbose_name='Situação (Ativo ou Desligado)',
        null=True, blank=True, default='Ativo'
    )

    erro_cep = models.CharField(max_length=255, blank=True, verbose_name='Erro ao buscar o CEP')

    def preencher_endereco_por_cep(self, request=None):
        try:
            url = f'https://api.postmon.com.br/v1/cep/{self.cep}'
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            self.logradouro = data.get('logradouro', '')
            self.bairro = data.get('bairro', '')
            self.cidade = data.get('cidade', '')
            self.uf = data.get('estado', '')
            self.erro_cep = ''

        except requests.RequestException as e:
            self.erro_cep = f'Erro ao buscar o CEP: {e}'
            self.logradouro = ''
            self.bairro = ''
            self.cidade = ''
            self.uf = ''
            if request:
                messages.error(request, self.erro_cep)

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.preencher_endereco_por_cep(request)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_membro if self.nome_membro else 'Membro sem nome'

    @staticmethod
    def aniversariantes_do_mes():
        mes_atual = date.today().month
        return MembroFinanceiro.objects.filter(data_aniversario__month=mes_atual)

    class Meta:
        verbose_name = "Cadastro de Membros"
        verbose_name_plural = "Cadastro de Membros"

class Autoreslivros(models.Model):
    nome_autor = models.CharField(max_length=80, unique=True, verbose_name='Nome do Autor')

    def __str__(self):
        return self.nome_autor

    class Meta:
        verbose_name = 'Autor do Livro'
        verbose_name_plural = 'Autor do Livro'

class Biblioteca(models.Model):
    titulo_livro = models.CharField(max_length=80, verbose_name='Título do Livro')
    nome_autor = models.ForeignKey(Autoreslivros, on_delete=models.CASCADE, verbose_name='Nome do Autor')
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código do Acervo', blank=True)
    categoria = models.CharField(max_length=80, verbose_name='Categoria do Livro', blank=True)
    qtdes_livros = models.BigIntegerField(verbose_name='Quantidade de Livros: ')
    local = models.CharField(max_length=80, verbose_name='Localização do Livro', blank=True)

    def __str__(self):
        return f"{self.titulo_livro} - {self.nome_autor}"

    class Meta:
        verbose_name = "Acervo da Biblioteca"
        verbose_name_plural = "Acervo da Biblioteca"

class EmprestimoLivro(models.Model):
    titulo_livro = models.ForeignKey(Biblioteca, on_delete=models.CASCADE, verbose_name='Título do Livro')
    nome_membro = models.ForeignKey(MembroFinanceiro, on_delete=models.CASCADE, verbose_name='Nome do Membro')
    data_emprestimo = models.DateTimeField(default=timezone.now, verbose_name='Data do Empréstimo')
    data_devolucao = models.DateTimeField(blank=True, null=True, verbose_name='Data da Devolução')

    def clean(self):
        """Validate that there is enough stock for the loan."""
        if self._state.adding:
            titulo_livro = Biblioteca.objects.get(id=self.titulo_livro.id)
            if titulo_livro.qtdes_livros < 1:
                raise ValidationError("Este livro não tem estoque para empréstimo.")

    def save(self, *args, **kwargs):
        logger.debug(f"Tentando salvar o empréstimo: {self.titulo_livro} para {self.nome_membro}")

        if self._state.adding:
            # Recarrega o objeto do banco de dados para garantir o valor mais atualizado
            titulo_livro = Biblioteca.objects.get(id=self.titulo_livro.id)
            logger.debug(f"Estoque atual do livro '{titulo_livro}': {titulo_livro.qtdes_livros}")

            # Verifica se há pelo menos um livro disponível
            if titulo_livro.qtdes_livros >= 1:
                titulo_livro.qtdes_livros -= 1
                titulo_livro.save()
                logger.debug(f"Novo estoque do livro '{titulo_livro}' após empréstimo: {titulo_livro.qtdes_livros}")
            else:
                logger.error(f"Erro: Livro '{titulo_livro}' não tem estoque para empréstimo.")
                raise ValidationError("Este livro não tem estoque para empréstimo.")
        elif self.data_devolucao is not None:
            if EmprestimoLivro.objects.filter(id=self.id, data_devolucao__isnull=True).exists():
                self.titulo_livro.qtdes_livros += 1
                self.titulo_livro.save()
                logger.debug(f"Novo estoque do livro '{self.titulo_livro}' após devolução: {self.titulo_livro.qtdes_livros}")

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('admin:index')

    def __str__(self):
        return f"{self.titulo_livro} emprestado para {self.nome_membro} em {self.data_emprestimo}"

    class Meta:
        verbose_name = "Empréstimo de Livro"
        verbose_name_plural = "Empréstimos de Livros"
        ordering = ['data_emprestimo']

class Patrimonio(models.Model):
    nome_patr = models.CharField(max_length=80, verbose_name='Nome do Patrimônio')
    codigo_patr = models.CharField(max_length=10, unique=True, verbose_name='Código do Patrimônio')
    cat_patr = models.CharField(max_length=80, blank=True, verbose_name='Categoria do Patrimônio')
    local_patr = models.CharField(max_length=80, blank=True, verbose_name='Local do Patrimônio')
    resp_patr = models.CharField(max_length=80, blank=True, verbose_name='Nome do Responsável')

    def __str__(self):
        return f"{self.nome_patr} - {self.codigo_patr}"

    class Meta:
        verbose_name = "Cadastro de Patrimônio"
        verbose_name_plural = "Cadastro de Patrimônio"

class Fornecedor(models.Model):
    nome_fornec = models.CharField(max_length=10, unique=True, verbose_name='Nome do Fornecedor')
    site = models.CharField(max_length=80, verbose_name='Endereço do Site', blank=True)
    cidade = models.CharField(max_length=80, verbose_name='Nome da Cidade', blank=True)
    telefone = models.CharField(max_length=80, verbose_name='Número do Telefone', blank=True)

    def __str__(self):
        return f"{self.nome_fornec} - {self.telefone}"

    class Meta:
        verbose_name = "Cadastro de Fornecedor"
        verbose_name_plural = "Cadastro de Fornecedor"

class BancoFinanceiro(models.Model):
    """Modelo para cadastro de bancos."""
    codigo_banco = models.AutoField(primary_key=True)
    nome_banco = models.CharField(max_length=255, verbose_name='Nome do Banco')
    numero_agencia = models.CharField(max_length=20, verbose_name='Número da Agência', blank=True)
    numero_conta = models.CharField(max_length=20, verbose_name='Número da Conta', blank=True)
    cidade_agencia = models.CharField(max_length=150, verbose_name='Cidade da Agência', blank=True)
    tipo_agencia = models.CharField(max_length=20, choices=[('matriz', 'Matriz'), ('filial', 'Filial'),('posto_avancado','Posto Avançado'),('Outros','Outros')],
                                    verbose_name='Tipo da Agência')
    titular = models.CharField(max_length=255, verbose_name='Titular da Conta', blank=True)
    data_cadastro = models.DateField(verbose_name='Data de Cadastro')
    observacoes = models.TextField(verbose_name='Observações', blank=True)

    def __str__(self):
        return self.nome_banco if self.nome_banco else 'Campo vazio'

    class Meta:
        verbose_name = "Cadastro de Bancos"
        verbose_name_plural = "Cadastro de Bancos"


class CadastroContas(models.Model):
    nome_conta = models.CharField(max_length=50, unique=True, verbose_name='Nome da Conta')
    nr_contabil = models.CharField(max_length=50, verbose_name='Número Contábil')

    def __str__(self):
        return f"{self.nome_conta} - {self.nr_contabil}"

    class Meta:
        verbose_name = "Cadastro de Contas"
        verbose_name_plural = "Cadastro de Contas"

class CadastroSubcontas(models.Model):
    nome_subconta = models.CharField(max_length=50, unique=True, verbose_name='Nome da Subconta')
    nr_subconta = models.CharField(max_length=50, verbose_name='Número Contábil da Subconta')

    def __str__(self):
        return f"{self.nome_subconta} - {self.nr_subconta}"

    class Meta:
        verbose_name = "Cadastro de Subcontas"
        verbose_name_plural = "Cadastro de Subcontas"

class ContasPagar(models.Model):
    nome_empresa = models.CharField(max_length=50, unique=True, verbose_name='Nome do Fornecedor')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    data_vencimento = models.DateField(verbose_name='Data do Vencimento')
    data_pagto = models.DateField(verbose_name='Data do Pagamento',blank=True)
    descricao = models.TextField(verbose_name='Descrição da Fatura:', help_text='Digite a descrição aqui: ', blank=True)

    def __str__(self):
        return f"{self.nome_empresa} - {self.valor}"

    class Meta:
        verbose_name = "Contas a Pagar"
        verbose_name_plural = "Contas a Pagar"


class MovimentoFinanceiro(models.Model):
    banco = models.ForeignKey(BancoFinanceiro, on_delete=models.CASCADE, verbose_name='Banco')
    tipo_conta = models.CharField(max_length=20, choices=[('corrente', 'Corrente'), ('poupanca', 'Poupança'), ('Outros', 'Outros')], verbose_name='Tipo de Conta')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    data_registro = models.DateField(verbose_name='Data do Registro')

    def __str__(self):
        return f"{self.banco}"  # ou qualquer campo que faça sentido para representar o objeto como string

    class Meta:
        verbose_name = "Depósito Bancário"
        verbose_name_plural = "Depósito Bancário"

class EntradaFinanceira(models.Model):
    nome_conta = models.ForeignKey(CadastroContas, on_delete=models.CASCADE, verbose_name='Contas')
    nome_subconta = models.ForeignKey(CadastroSubcontas, on_delete=models.CASCADE, verbose_name='Nome da Subconta')
    banco = models.ForeignKey(BancoFinanceiro, on_delete=models.CASCADE, verbose_name='Nome do Banco')
    descricao = models.TextField(verbose_name='Descrição da Entrada:', help_text='Digite a descrição aqui: ', blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor da Entrada')
    data_entrada = models.DateField(verbose_name='Data da Entrada')

    def __str__(self):
        return f"{self.descricao} - {self.nome_conta}"

    class Meta:
        verbose_name = "Entrada de Valores"
        verbose_name_plural = "Entradas de Valores"

class SaidaFinanceira(models.Model):
    nome_conta = models.ForeignKey(CadastroContas, on_delete=models.CASCADE, verbose_name='Nome da Conta')
    nome_subconta = models.ForeignKey(CadastroSubcontas, on_delete=models.CASCADE, verbose_name='Nome da Subconta')
    banco = models.ForeignKey(BancoFinanceiro, on_delete=models.CASCADE, verbose_name='Nome do Banco')
    descricao = models.TextField(verbose_name='Descrição do Pagamento:', help_text='Digite a descrição aqui: ', blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor do Pagamento')
    data_saida = models.DateField(verbose_name='Data do Pagamento')

    def __str__(self):
        return f"{self.descricao} - {self.nome_conta}- {self.nome_subconta}"

    class Meta:
        verbose_name = "Pagamentos Realizados"
        verbose_name_plural = "Pagamentos Realizados"

class BalanceteMensal(models.Model):
    mes = models.IntegerField()
    ano = models.IntegerField()
    total_entradas = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, verbose_name='Total de Entrada')
    total_saidas = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, verbose_name='Total de Pagamentos')
    saldo_mensal = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, verbose_name='Saldo Mensal')

    class Meta:
        verbose_name = "Balancete Mensal"
        verbose_name_plural = "Balancetes Mensal"

class SaldoAnual(models.Model):
    ano = models.IntegerField()
    total_entradas_ano = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name='Total de Entrada/Ano')
    total_saidas_ano = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name='Total de Pagamentos/Ano')
    saldo_anual = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name='Saldo Anual')

    class Meta:
        verbose_name = "Saldo Anual"
        verbose_name_plural = "Saldo Anual"

@receiver(post_save, sender=EntradaFinanceira)
@receiver(post_save, sender=SaidaFinanceira)
def atualizar_balancete_mensal_mes(sender, instance, **kwargs):
    mes = instance.data_entrada.month if sender == EntradaFinanceira else instance.data_saida.month
    ano = instance.data_entrada.year if sender == EntradaFinanceira else instance.data_saida.year
    balancete_mensal, _ = BalanceteMensal.objects.get_or_create(mes=mes, ano=ano)
    entradas_mensais = EntradaFinanceira.objects.filter(data_entrada__month=mes, data_entrada__year=ano).aggregate(
        total_entradas=Sum('valor'))['total_entradas'] or 0
    saidas_mensais = SaidaFinanceira.objects.filter(data_saida__month=mes, data_saida__year=ano).aggregate(
        total_saidas=Sum('valor'))['total_saidas'] or 0
    balancete_mensal.total_entradas = entradas_mensais
    balancete_mensal.total_saidas = saidas_mensais
    balancete_mensal.saldo_mensal = entradas_mensais - saidas_mensais
    balancete_mensal.save()
    atualizar_balancete_anual_ano(ano)

def atualizar_balancete_anual_ano(ano):
    saldo_anual, _ = SaldoAnual.objects.get_or_create(ano=ano)
    entradas_anuais = EntradaFinanceira.objects.filter(data_entrada__year=ano).aggregate(
        total_entradas_ano=Sum('valor'))['total_entradas_ano'] or 0
    saidas_anuais = SaidaFinanceira.objects.filter(data_saida__year=ano).aggregate(
        total_saidas_ano=Sum('valor'))['total_saidas_ano'] or 0
    saldo_anual.total_entradas_ano = entradas_anuais
    saldo_anual.total_saidas_ano = saidas_anuais
    saldo_anual.saldo_anual = entradas_anuais - saidas_anuais
    saldo_anual.save()
