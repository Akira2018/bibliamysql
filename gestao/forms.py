from django import forms
from .models import Biblia

from .models import (
    EntradaFinanceira, SaidaFinanceira, BalanceteMensal,
    SaldoAnual, Cadastroestudos, Agendapastoral, Agendaigreja,
    MembroFinanceiro, Batismoigreja
)

class BibliaForm(forms.Form):
    nome_livro = forms.ModelChoiceField(queryset=Biblia.objects.all(), label="Livro")
    capitulo = forms.IntegerField(min_value=1, label="Capítulo")

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, label="Buscar na Bíblia")

class CadastroestudosForm(forms.ModelForm):
    class Meta:
        model = Cadastroestudos
        fields = ['titulo', 'descricao', 'data_registro']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'data_registro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AgendapastoralForm(forms.ModelForm):
    class Meta:
        model = Agendapastoral
        fields = ['descricao', 'data_evento']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'data_evento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AgendaigrejaForm(forms.ModelForm):
    class Meta:
        model = Agendaigreja
        fields = ['descricao', 'data_evento']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'data_evento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class BatismoigrejaForm(forms.ModelForm):
    class Meta:
        model = Batismoigreja
        fields = ['nome', 'data_batismo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'size': '200'}),
            'data_batismo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class MembroFinanceiroForm(forms.ModelForm):
    class Meta:
        model = MembroFinanceiro
        fields = [
            'nome_membro', 'data_aniversario', 'estado_civil', 'cargo', 'grupo', 'email', 'cpf', 'rg',
            'cep', 'logradouro', 'complemento', 'bairro', 'cidade', 'uf', 'nr_imovel', 'observacao', 'nome_prof',
            'nome_habilidade', 'numero_telefone', 'situacao', 'erro_cep', 'foto'
        ]
        widgets = {
            'nome_membro': forms.TextInput(attrs={'class': 'form-control wide-input'}),
            'foto': forms.FileInput(attrs={'class': 'form-control-file'}),
            'data_aniversario': forms.DateInput(attrs={'class': 'form-control wide-input', 'type': 'date'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control wide-select'}),
            'cargo': forms.Select(attrs={'class': 'form-control wide-select'}),
            'grupo': forms.Select(attrs={'class': 'form-control wide-select'}),
            'nome_prof': forms.Select(attrs={'class': 'form-control wide-select'}),
            'nome_habilidade': forms.Select(attrs={'class': 'form-control wide-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control wide-input'}),
            'numero_telefone': forms.TextInput(attrs={'class': 'form-control wide-input'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control wide-input'}),
            'rg': forms.TextInput(attrs={'class': 'form-control wide-input'}),
            'cep': forms.TextInput(attrs={'class': 'form-control wide-input'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control wide-input'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control wide-input'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control wide-input'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control wide-input'}),
            'uf': forms.Select(attrs={'class': 'form-control wide-select'}),
            'nr_imovel': forms.TextInput(attrs={'class': 'form-control wide-input'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control wide-input'}),
            'situacao': forms.Select(attrs={'class': 'form-control wide-select'}),
            'erro_cep': forms.TextInput(attrs={'class': 'form-control wide-input', 'readonly': 'readonly'}),
        }

class EntradaFinanceiraForm(forms.ModelForm):
    class Meta:
        model = EntradaFinanceira
        fields = ['descricao', 'valor', 'data_entrada']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_entrada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class SaidaFinanceiraForm(forms.ModelForm):
    class Meta:
        model = SaidaFinanceira
        fields = ['descricao', 'valor', 'data_saida']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_saida': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class BalanceteMensalForm(forms.ModelForm):
    class Meta:
        model = BalanceteMensal
        fields = ['mes', 'ano', 'total_entradas', 'total_saidas', 'saldo_mensal']
        widgets = {
            'mes': forms.NumberInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_entradas': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_saidas': forms.NumberInput(attrs={'class': 'form-control'}),
            'saldo_mensal': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SaldoAnualForm(forms.ModelForm):
    class Meta:
        model = SaldoAnual
        fields = ['ano', 'total_entradas_ano', 'total_saidas_ano', 'saldo_anual']
        widgets = {
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_entradas_ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_saidas_ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'saldo_anual': forms.NumberInput(attrs={'class': 'form-control'}),
        }