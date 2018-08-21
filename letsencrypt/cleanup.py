#! /usr/bin/python
# -*- encoding: utf-8 -*-

import os
from api_dns import *

def cleanup():
    chall_hash =  os.getenv('CERTBOT_VALIDATION')
    dominio = os.getenv('CERTBOT_DOMAIN')
    chall_url = ("_acme-challenge.%s" % dominio)
    clean = excluir_entrada(dominio, chall_url, 'txt', chall_hash)

if __name__ == '__main__':
    cleanup()
