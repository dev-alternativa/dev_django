from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()

# Flag de ambienet
ENVIRONMENT = os.getenv('ENVIRONMENT', 'DEV').strip().upper()

ENVIRONMENT_DEV = ENVIRONMENT == 'DEV'
ENVIRONMENT_HML = ENVIRONMENT == 'HML'
ENVIRONMENT_PRD = ENVIRONMENT == 'PRD'


CNPJ_API_ENDPOINT = os.getenv('CNPJ_API_ENDPOINT', 'https://publica.cnpj.ws/cnpj/')
CEP_API_ENDPOINT = os.getenv('CEP_API_ENDPOINT', 'https://brasilapi.com.br/api/cep/v2/')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cw-0x)y_b9)a!h)l&0xlx^k!5y_rchz6@a$u*!e*_oz53u6=n!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '192.168.15.149',
    'altflexo.site',
    'www.altflexo.site',
    '162.240.229.32',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # libs
    'django_bootstrap5',
    'crispy_forms',
    'crispy_bootstrap5',
    'import_export',
    'django_select2',
    'crispy_formset_modal',
    'rest_framework',
    # my apps
    'accounts',
    'api',
    'api_omie',
    'core',
    'common',
    'imports',
    'logistic',
    'products',
    'transactions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'altflex.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # carrega variáveis de ambientes no contexto de templates
                'core.context_processors.environment_variables',
            ],
        },
    },
]

WSGI_APPLICATION = 'altflex.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'hml_database'),
        'USER': os.getenv('MYSQL_USER', 'alt'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'Alt@123hml'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
        },
    }
}


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

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "core/static"),
]
MEDIA_URL = '/media/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'


# Configuração de armazenamento das mensagens
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Configuração de autoincremento de IDs
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração de autenticação de usuários
AUTH_USER_MODEL = 'accounts.CustomUsuario'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = 'index'   # A página para onde o usuário será redirecionado após fazer login
LOGOUT_REDIRECT_URL = 'login'  # A página para onde o usuário será redirecionado após fazer logout

LOGIN_URL = 'login'
SELECT2_CSS = ['css/select2.css']
