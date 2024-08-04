from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from django.conf import settings
from django.http import HttpResponse, Http404
import os
import qrcode
from .models import Batismoigreja, MembroFinanceiro, EntradaFinanceira, SaidaFinanceira, BalanceteMensal, SaldoAnual
from .forms import EntradaFinanceiraForm, SaidaFinanceiraForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.db.models import Sum
from django.views.generic import ListView
from .models import EntradaFinanceira
from django_excel import make_response_from_query_sets
from .models import SaidaFinanceira
import logging
from django.core.paginator import Paginator
from .models import Biblia
from django.http import JsonResponse
from reportlab.lib.styles import TA_CENTER
from reportlab.lib.styles import TA_JUSTIFY
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from .bible_books import BIBLE_BOOKS_ORDER

# Configure o logger
logger = logging.getLogger(__name__)

def get_chapters(request):
    book_name = request.GET.get('book')
    if book_name:
        chapters = Biblia.objects.filter(nome_livro=book_name).values_list('capitulo', flat=True).distinct().order_by('capitulo')
        chapter_options = '<option value="">Selecione um capítulo</option>'
        for chapter in chapters:
            chapter_options += f'<option value="{chapter}">{chapter}</option>'
        return JsonResponse({'chapter_options': chapter_options})
    return JsonResponse({'chapter_options': '<option value="">Selecione um capítulo</option>'})

def profile_view(request):
    return render(request, 'profile.html')

def book_chapter_view(request, book_id, chapter_id):
    verses = Biblia.objects.filter(nome_livro=book_id, capitulo=chapter_id)
    if not verses:
        return render(request, '404.html', status=404)
    return render(request, 'book_chapter.html', {'verses': verses})

def verse_list_view(request):
    versiculos = Biblia.objects.all()
    return render(request, 'verse_list.html', {'versiculos': versiculos})


def home(request):
    livros = Biblia.objects.values('nome_livro').distinct()  # Pega apenas os nomes dos livros únicos
    return render(request, 'home.html', {'livros': livros})

def Biblia_view(request, book_id, chapter_id):
    livro = get_object_or_404(Biblia, nome_livro=book_id, capitulo=chapter_id)
    versiculos = Biblia.objects.filter(nome_livro=book_id, capitulo=chapter_id)
    return render(request, 'book_chapter.html', {'livro': livro, 'versiculos': versiculos})

# Lista com a ordem correta dos livros da Bíblia
BIBLE_BOOKS_ORDER = [
    'Gênesis', 'Êxodo', 'Levítico', 'Números', 'Deuteronômio',
    'Josué', 'Juízes', 'Rute', 'I Samuel', 'II Samuel',
    'I Reis', 'II Reis', 'I Crônicas', 'II Crônicas', 'Esdras',
    'Neemias', 'Ester', 'Jó', 'Salmos', 'Provérbios',
    'Eclesiastes', 'Cantares', 'Isaías', 'Jeremias', 'Lamentações',
    'Ezequiel', 'Daniel', 'Oseias', 'Joel', 'Amós',
    'Obadias', 'Jonas', 'Miqueias', 'Naum', 'Habacuque',
    'Sofonias', 'Ageu', 'Zacarias', 'Malaquias', 'Mateus',
    'Marcos', 'Lucas', 'João', 'Atos', 'Romanos',
    'I Coríntios', 'II Coríntios', 'Gálatas', 'Efésios', 'Filipenses',
    'Colossenses', 'I Tessalonicenses', 'II Tessalonicenses', 'I Timóteo', 'II Timóteo',
    'Tito', 'Filemom', 'Hebreus', 'Tiago', 'I Pedro',
    'II Pedro', 'I João', 'II João', 'III João', 'Judas',
    'Apocalipse'
]

def search_view(request):
    # Extrair parâmetros da query string
    book = request.GET.get('book', '')
    chapter = request.GET.get('chapter', '')
    word = request.GET.get('word', '')

    # Filtragem e busca
    queryset = Biblia.objects.all()
    if book:
        queryset = queryset.filter(nome_livro=book)
    if chapter and chapter.isdigit():
        queryset = queryset.filter(capitulo=int(chapter))
    if word:
        queryset = queryset.filter(texto_biblico__icontains=word)

    # Ordenação e paginação
    queryset = queryset.order_by('nome_livro', 'capitulo', 'versiculo')
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Passar a lista de livros para o template
    context = {
        'verses': page_obj.object_list,
        'page_obj': page_obj,
        'books': BIBLE_BOOKS_ORDER,
        'chapters': range(1, 151),  # Ajuste se necessário
    }
    return render(request, 'search.html', context)

# Função para gerar certificado de batismo
def gerar_certificado_batismo(request, batismo_id):
    try:
        batismo = Batismoigreja.objects.get(id=batismo_id)
    except Batismoigreja.DoesNotExist:
        raise Http404("O registro de Batismo não existe.")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_batismo_{batismo_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Adicionar imagem à esquerda da página
    logo_path = settings.IMAGEM_IGREJA
    if logo_path and os.path.exists(logo_path):
        logo_image = Image(logo_path, width=40, height=40)
        elements.append(logo_image)

    elements.append(Spacer(1, 80))

    # Adicionar título grande e centralizado
    titulo = "Certificado de Batismo"
    titulo_style = ParagraphStyle(name='Titulo', alignment=TA_CENTER, fontSize=20, spaceAfter=36, bold=True)
    elements.append(Paragraph(titulo, titulo_style))

    elements.append(Spacer(1, 12))

    # Adicionar texto do certificado justificado
    text = f"""Certificamos que o(a) irmão(a) {batismo.nome} foi batizado(a) em nome do Pai, do Filho e do Espírito Santo no dia {batismo.data_batismo.strftime('%d/%m/%Y')} 
na Igreja Vineyard de Bauru, situada na Rua Aviador Gomes Ribeiro, Quadra 31 - Vila Cardia, Bauru - SP, 17011-067.

O batismo é a primeira ordenança do evangelho. Uma das instruções que o Senhor ensinou a Seus Apóstolos foi:

"19 - Portanto ide, fazei discípulos de todas as nações, batizando-os em nome do Pai, e do Filho, e do Espírito Santo;
20 - Ensinando-os a guardar todas as coisas que eu vos tenho mandado; e eis que eu estou convosco todos os dias, até a consumação dos séculos. Amém. Mateus 28:19-20"""
    text_style = ParagraphStyle(name='Justificado', alignment=TA_JUSTIFY)
    elements.append(Paragraph(text, text_style))

    elements.append(Spacer(1, 50))

    # Gerar QR code
    qr_text = f"Igreja Vineyard de Bauru - Pastor Eduardo Davi Asckar - Certificado de Batismo \n{batismo.nome}\n{batismo.data_batismo.strftime('%d/%m/%Y')}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')

    # Salvar QR code em um arquivo temporário
    qr_img_path = os.path.join(settings.MEDIA_ROOT, 'qr_temp.png')
    qr_img.save(qr_img_path)

    qr_image = Image(qr_img_path, width=135, height=135)
    elements.append(qr_image)

    smaller_text = "Use a câmera do celular para ler o QR Code"
    smaller_text_style = ParagraphStyle(name='SmallerText', alignment=TA_CENTER, fontSize=6)
    elements.append(Paragraph(smaller_text, smaller_text_style))

    doc.build(elements)

    # Remover o arquivo temporário do QR code
    os.remove(qr_img_path)

    return response

from django.shortcuts import render

def home(request):
    return render(request, 'gestao/home.html')

def criar_batismo(request):
    if request.method == 'POST':
        form = BatismoigrejaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Batismo cadastrado com sucesso!')
            return redirect('criar_batismo')
    else:
        form = BatismoigrejaForm()

    return render(request, 'cadastrobatismo.html', {'form': form})

def aniversariantes(request):
    aniversariantes = list(MembroFinanceiro.aniversariantes_do_mes())
    aniversariantes.sort(key=lambda x: (x.data_aniversario.month, x.data_aniversario.day))

    context = {'aniversariantes': aniversariantes}
    return render(request, 'aniversariantes.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def adicionar_entrada(request):
    if request.method == 'POST':
        form = EntradaFinanceiraForm(request.POST)
        if form.is_valid():
            entrada = form.save()
            atualizar_balancete_mensal_mes(entrada.data_entrada.month, entrada.data_entrada.year)
            atualizar_balancete_anual_ano(entrada.data_entrada.year)
            return redirect('home')
    else:
        form = EntradaFinanceiraForm()
    return render(request, 'adicionar_entrada.html', {'form': form})

def adicionar_saida(request):
    if request.method == 'POST':
        form = SaidaFinanceiraForm(request.POST)
        if form.is_valid():
            saida = form.save()
            atualizar_balancete_mensal_mes(saida.data_saida.month, saida.data_saida.year)
            atualizar_balancete_anual_ano(saida.data_saida.year)
            return redirect('home')
    else:
        form = SaidaFinanceiraForm()
    return render(request, 'adicionar_saida.html', {'form': form})

def atualizar_balancete_mensal_mes(mes, ano):
    balancete_mensal, _ = BalanceteMensal.objects.get_or_create(mes=mes, ano=ano)
    entradas_mensais = EntradaFinanceira.objects.filter(data_entrada__month=mes, data_entrada__year=ano).aggregate(total_entradas=Sum('valor'))['total_entradas'] or 0
    saidas_mensais = SaidaFinanceira.objects.filter(data_saida__month=mes, data_saida__year=ano).aggregate(total_saidas=Sum('valor'))['total_saidas'] or 0
    balancete_mensal.total_entradas = entradas_mensais
    balancete_mensal.total_saidas = saidas_mensais
    balancete_mensal.saldo_mensal = entradas_mensais - saidas_mensais
    balancete_mensal.save()

def atualizar_balancete_anual_ano(ano):
    saldo_anual, _ = SaldoAnual.objects.get_or_create(ano=ano)
    entradas_anuais = EntradaFinanceira.objects.filter(data_entrada__year=ano).aggregate(total_entradas_ano=Sum('valor'))['total_entradas_ano'] or 0
    saidas_anuais = SaidaFinanceira.objects.filter(data_saida__year=ano).aggregate(total_saidas_ano=Sum('valor'))['total_saidas_ano'] or 0
    saldo_anual.total_entradas_ano = entradas_anuais
    saldo_anual.total_saidas_ano = saidas_anuais
    saldo_anual.saldo_anual = entradas_anuais - saidas_anuais
    saldo_anual.save()

def export_balancete_mensal_to_excel(request):
    # Supondo que você tenha uma lógica para gerar o balancete mensal
    data = {...}  # Dados para exportar
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Balancete Mensal')
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=balancete_mensal.xlsx'
    return response


class MembroFinanceiroListView(ListView):
    model = MembroFinanceiro
    template_name = 'membros/membro_list.html'
    context_object_name = 'membros'

def export_entradas(request):
    entradas = EntradaFinanceira.objects.all()
    return make_response_from_query_sets([entradas], 'xlsx', file_name='entradas')

def export_saidas(request):
    saidas = SaidaFinanceira.objects.all()
    return make_response_from_query_sets([saidas], 'xlsx', file_name='saidas')



