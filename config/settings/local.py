from config.settings.base import *

ALLOWED_HOSTS = ["*"]


# DATA BASE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portfolio',
        'USER': 'jhn',
        'PASSWORD': '1q2w3e4r',
        'HOST': 'localhost',  # Docker 컨테이너 내부에서 실행할 경우 "db"
        'PORT': '5432',
    }
}