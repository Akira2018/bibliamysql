import os
from pathlib import Path
import django_heroku
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-li1dd3ijq(uutb#ksg*-u++-xqrs8b_h&r3wobp2^v0snk&wha'

# Configuração da conexão com o Docker Engine
#DOCKER_BASE_URL = 'unix://var/run/docker.sock'  # ou 'tcp://127.0.0.1:2375' para conexão remota
DOCKER_BASE_URL = 'TCP://127.0.0.1:2375' ##para conexão remota
DOCKER_API_VERSION = 'auto'  # para detectar automaticamente a versão da API Docker

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

ADMIN_URL = 'admin/'  # Defina o URL do painel de administração
LOGIN_URL = '/accounts/login/'
CSRF_COOKIE_SECURE = False  # Defina como True se estiver usando HTTPS

CSRF_TRUSTED_ORIGINS = ['https://gestao-4a352bdcd142.herokuapp.com/']

# Define o tempo de expiração da sessão em segundos (por exemplo, 1 hora)
SESSION_COOKIE_AGE = 3600

#APP_NAME = os.environ.get("FLY_APP_NAME")  # Application definition

# settings.py

import os

LOGIN_REDIRECT_URL = '/accounts/profile/'

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configurações para arquivos estáticos
#STATIC_URL = '/static/'
#STATICFILES_DIRS = [BASE_DIR / "static"]
#STATIC_ROOT = BASE_DIR / "staticfiles"

# Configurar o diretório dos arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Configuração de Logging
# Configuração de Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Configure TEMPLATE_DIR
TEMPLATE_DIR = os.path.join(BASE_DIR, 'gestao/templates')

# Configuração dos Templates
import os
from pathlib import Path  # Importe pathlib para lidar com caminhos

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configure TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'gestao', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'grappelli',
    'gestao',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    'http://localhost',  # Incluído o esquema e a porta, se aplicável
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_HEADERS = [
    'Accept',
    'Accept-Language',
    'Content-Language',
    'Content-Type',
    'Authorization',
]

SUIT_CONFIG = {
    'ADMIN_NAME': 'Django administration',
    'MENU': (
        'sites',
        {'label': 'Custom', 'icon': 'icon-cog', 'models': ('auth.user', 'auth.group')},
        {'label': 'Blog', 'icon': 'icon-book', 'models': ('blog.category', 'blog.post')},
    )
}


ROOT_URLCONF = 'gestao.urls'

WSGI_APPLICATION = 'gestao_proj.wsgi.application'

# Configuração do banco de dados para ambiente local (Windows)
#if os.name == 'nt':
#    DATABASE_PATH = os.path.join(BASE_DIR, 'Cadastro.sqlite3')
# Configuração do banco de dados para ambiente de produção (fly.io)
#else:
#    DATABASE_PATH = "/mnt/db-prod.db"
# Configurações do Banco de Dados


import os
from urllib.parse import urlparse
import dj_database_url

import os

ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('CLEARDB_DATABASE_URL')
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'bdgestao.sqlite3'),
        }
    }

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'bdbiblia',
#        'USER': 'root',
#        'PASSWORD': 'Bauru2024',
#        'HOST': 'localhost',  # ou o endereço do seu servidor de banco de dados
#        'PORT': '3306',  # a porta padrão do MySQL
#    }
#}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# Outras configurações
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = False
USE_TZ = True

import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações do Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configurações do Banco de Dados
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'bdgestao.sqlite3',
#    }
#}

# Arquivos de Mídia (Imagens)
#MEDIA_ROOT = BASE_DIR / 'media'
#MEDIA_URL = '/media/'
#DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Arquivos de Mídia (Imagens)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMAGEM_IGREJA = os.path.join(MEDIA_ROOT, 'igreja', 'imagemvineyard.jpg')

SQLITE3_ROOT = os.path.join(BASE_DIR, 'sqlite3')
SQLITE3_URL = "/venv/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

django_heroku.settings(locals())
