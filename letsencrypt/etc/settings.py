# -*- coding: utf-8 -*-

import os

### Configurações do celery ###
#broker = 'amqp://guest@172.17.0.2//'
#backend = 'amqp://guest@172.17.0.2//'
broker = os.environ.get('BROKER_URL')
backend = os.environ.get('BROKER_URL')

### Lista de NS que podem ser utilizados pelo validator ###
lista_soa = []

### Dicionário do status_json ###
schema_json = {
    'status': 'iniciando',
}

### Configurações do validator intervalo em segs e tentativas ###
intervalo = 30
max_retry = 20

### diretório onde o validator e outros salvam o status_json ###
status_json_dir = '/var/www/html/certs'
