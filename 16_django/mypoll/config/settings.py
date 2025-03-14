"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p@r2e9rs$fmm=%#x*8!tk@u##!@n)g9wfid7m1u8@xh2kn@xru'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "polls",
    "account",
    "django_bootstrap5",
]
    
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "config.middleware.NoCacheMiddleware",  # logout back시 처리를 위한 cache 처리
]

ROOT_URLCONF = 'config.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

##############################
# 사용자 정의 User 모델 등록
##############################
AUTH_USER_MODEL = "account.User"  # AbstractUser 클래스 등록

##################
# 로그인 관련설정
##################
# 로그인 안한 사용자가 로그인해야 실행할 수있는 View를 호출 했을때 
#                        이동할 url 설정.
LOGIN_URL = '/account/login' 

# 로그인/로그아웃 처리후에 이동할 url - Class기반 View를 사용할 때 필요
LOGIN_REDIRECT = '/'
LOGOUT_REDIRECT = '/'

#############################################################
# static 파일 (html에서 사용할 image, js, css, ... 파일들) 설정
#  1. app/static 아래 저장 -> static 파일들을 자동으로 장고서버가 인식
#  2. 1이외 경로에 static 파일을 저장 -> setting.py에 설정.
#############################################################
# static파일을 client에서 요청할 때 사용할 url의 시작 path.
# account/static/account/img/join.jpg
# html: <img src="/static/account/img/join.jpg">
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static_files',]

STATIC_ROOT = BASE_DIR / 'static_collection'
# python manage.py collectstatic
## app/static, staticfiles_dirs 디렉토리들에 있는 static 파일들을
##     STATIC_ROOT 디렉토리 아래로 모아준다.

# - 운영환경
## http 서버 + wsgi(django실행환경) 나눠서 서버를 구축할 때
## http 서버가 static 파일 요청을 처리. 
##  static 파일들의 경로를 http서버에게 알려줘야 한다.
##  static 파일들을 한 디렉토리(STATIC_ROOT)에 모은 뒤 그 디렉토리를 알려준다.
# http서버: apache httpd, nginx

##################
# MEDIA 설정
##################
MEDIA_ROOT = BASE_DIR / "media" # 업로드 파일 저장 디렉토리
MEDIA_URL = "/media/" # 업로드 파일 요청할 시작 url
