#! /usr/bin/python
# -*- coding: utf-8 -*-

import time, logging
from oper_status_json import *
from api_dns import *
from dns_query import *
from sys import argv
from etc.settings import schema_json, intervalo, max_retry, status_json_dir

chall_hash =  os.getenv('CERTBOT_VALIDATION')
dominio = os.getenv('CERTBOT_DOMAIN')
chall_url = ("_acme-challenge.%s" % dominio)
dominio_raiz = retorna_root_domain(dominio)
status_path = argv[1]

logging.basicConfig(filename='/tmp/validator.log', level=logging.DEBUG)

def verify_hash(chall_hash, chall_url=chall_url):
    logging.info('verificando hash: %s  url: %s' % (chall_hash, chall_url))
    status_json['nameservers'] = retorna_lista_ns(dominio)
    return_hash = retorna_lista_txt(chall_url)
    logging.info('hash encontrados no dns: %s' % (return_hash))
    if chall_hash in return_hash:
        status_json['entrada TXT atual'] = return_hash
        write_status_json(status_json, json_file)
        return True
    else:
        status_json['entrada TXT atual'] = return_hash
        write_status_json(status_json, json_file)
        return False

def hash_validation(status_json, json_file, chall_url=chall_url):
    logging.info('hash validation...')
    status_json['status'] = 'validando hash'
    status_json['validando dominio'] = dominio
    status_json[u'hash de validação'] = chall_hash
    status_json['challenge url'] = chall_url
    status_json['tentativas'] = 00
    write_status_json(status_json, json_file)
    while verify_hash(chall_hash) == False and status_json['tentativas'] < max_retry:
        time.sleep(intervalo)
        status_json['tentativas'] += 01
        write_status_json(status_json, json_file)
    if status_json['tentativas'] == max_retry:
        status_json['status'] = 'max retry'
        status_json['erro'] = 'atingido número máximo de tentativas'
        write_status_json(status_json, json_file)
    else:
        status_json['status'] = 'verificação concluída'
        write_status_json(status_json, json_file)
    del_status_json('entrada TXT atual', json_file)
    del_status_json('tentativas', json_file)
    del_status_json(u'hash de validação', json_file)
    del_status_json(u'nameservers', json_file)
    del_status_json('challenge url', json_file)
    del_status_json('validando dominio', json_file)

if __name__ == '__main__':
    json_file = create_file(status_path, schema_json, status_json_dir)

    logging.info("""iniciando o validator\n
        dominio: %s
        dominio_raiz: %s
        chall_hash: %s
        chall_url: %s
        json_file: %s
        """ % (dominio, dominio_raiz, chall_hash, chall_url, json_file))
    status_json = read_status_json(json_file)

    status_json['status'] = 'Criando entrada no DNS'
    write_status_json(status_json, json_file)
    create_dns_hash = criar_entrada(dominio_raiz, chall_url, 'txt', chall_hash)
    logging.info('criando entrada dns %s' % create_dns_hash['mensagem'])
    status_json['criação da entrada no dns'] = create_dns_hash['mensagem']

    logging.info('escrevendo no arquivo: %s' % json_file)
    write_status_json(status_json, json_file)
    hash_validation(status_json, json_file)
