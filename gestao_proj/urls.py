from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from . import views  # Importe todo o módulo views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('export_balancete_mensal/', views.export_balancete_mensal, name='export_balancete_mensal'),
    path('export_entradas/', views.export_entradas, name='export_entradas'),
    path('export_saidas/', views.export_saidas, name='export_saidas'),
    path('aniversariantes/', views.aniversariantes, name='aniversariantes'),
    path('cadastrobatismo/', views.criar_batismo, name='criar_batismo'),
    path('certificado_batismo/<int:batismo_id>/', views.gerar_certificado_batismo, name='certificado_batismo'),
    path('', views.index, name='index'),
    path('', include('gestao.urls')),  # Inclui as URLs do seu aplicativo
    path('bible/search/', views.search_view, name='search'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

