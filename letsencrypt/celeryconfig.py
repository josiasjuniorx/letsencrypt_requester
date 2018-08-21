# -*- coding: utf-8 -*-

from datetime import timedelta
from etc.settings import broker, backend

BROKER_URL = broker
CELERY_RESULT_BACKEND = backend
CELERY_INCLUDE = ['letsencrypt.letsencrypt_requester', 'letsencrypt.get_status']
CELERY_ACCEPT_CONTENT = ['application/x-python-serialize', 'application/json']
#CELERY_TASK_SERIALIZER = ['pickle', 'json']
#CELERY_RESULT_SERIALIZER = ['pickle', 'json']

CELERYBEAT_SCHEDULE = {
    'Atualizando Status dos Certificados': {
        'task': 'letsencrypt.get_status.gera_status',
        'schedule': timedelta(seconds=300)
    },
}
