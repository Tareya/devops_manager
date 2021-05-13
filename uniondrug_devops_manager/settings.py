"""
Django settings for uniondrug_devops_manager project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

'''Basic Configuration'''
# 加载数据库配置
import pymysql
pymysql.install_as_MySQLdb()

# 加载 apps 路径
import logging, os, sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 识别apps目录路径
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dx^to$8cc=7cm=&k5-qkb+q389%p56^+pujnsb!)6dbm^!k2wv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = "*"


'''LDAP Configuration'''
import ldap 
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, ActiveDirectoryGroupType


#修改Django认证先走ldap，再走本地认证
AUTHENTICATION_BACKENDS = (
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
)

#ldap的连接基础配置
AUTH_LDAP_SERVER_URI = "ldap://192.168.3.253:389"
AUTH_LDAP_BIND_DN = "CN=ldap-services,CN=Users,DC=uniondrug,DC=com"
AUTH_LDAP_BIND_PASSWORD = 'P@ssw0rd@1qaz'

#允许认证用户的路径
AUTH_LDAP_USER_SEARCH = LDAPSearch("OU=UniondrugUsers,DC=uniondrug,DC=com", ldap.SCOPE_SUBTREE,
                                   "(sAMAccountName=%(user)s)")
#通过组进行权限控制
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("OU=UniondrugGroups,DC=uniondrug,DC=com", ldap.SCOPE_SUBTREE,
                                    "(objectClass=groupOfNames)")

# 定义LDAP模式
# AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
# #is_staff:这个组里的成员可以登录；is_superuser:组成员是django admin的超级管理员；is_active:组成员可以登录django admin后台，但是无权限查看后台内容
# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#  "is_staff": "cn=test_users,ou=groups,OU=test,DC=test,DC=com",
#  "is_superuser": "cn=test_users,ou=groups,OU=tset,DC=test,DC=com",
# }
# #通过组进行权限控制end

# AD LDAP 模式
AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType()
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 1,
    ldap.OPT_REFERRALS: 0,
}

#当ldap用户登录时，从ldap的用户属性对应写到django的user数据库，键为django的属性，值为ldap用户的属性
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

#如果为True，每次组成员都从ldap重新获取，保证组成员的实时性；反之会对组成员进行缓存，提升性能，但是降低实时性
# AUTH_LDAP_FIND_GROUP_PERMS = True



# Application definition

INSTALLED_APPS = [
    'simpleui',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uniondrug_devops_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'uniondrug_devops_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'uniondrug_devops_manager',
        'USER': 'uniondrug',
        'PASSWORD': '%I!g69kvtye%Ne73',
        'HOST': '47.99.195.100',
        'PORT': 13306,
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB;'
        }
    }
}

# 新版drf schema_class默认用的是rest_framework.schemas.openapi.AutoSchema
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': {
        'rest_framework.schemas.coreapi.AutoSchema',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    },
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")