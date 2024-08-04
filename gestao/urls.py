from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from . import views  # Importe todo o módulo views

urlpatterns = [
    path('admin/', admin.site.urls),  # Adiciona a URL do admin
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('export_balancete_mensal/', views.export_balancete_mensal_to_excel, name='export_balancete_mensal'),
    path('export_entradas/', views.export_entradas, name='export_entradas'),
    path('export_saidas/', views.export_saidas, name='export_saidas'),
    path('aniversariantes/', views.aniversariantes, name='aniversariantes'),
    path('cadastrobatismo/', views.criar_batismo, name='criar_batismo'),
    path('certificado_batismo/<int:batismo_id>/', views.gerar_certificado_batismo, name='certificado_batismo'),
    path('membros/', views.MembroFinanceiroListView.as_view(), name='gestao_membrofinanceiro_changelist'),
    path('bible/search/', views.search_view, name='search_view'),
    path('bible/verses/', views.verse_list_view, name='verse_list'),
    path('book/<int:book_id>/chapter/<int:chapter_id>/', views.book_chapter_view, name='book_chapter'),
    path('bible/chapters/', views.get_chapters, name='get_chapters'),  # Nova URL

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)































