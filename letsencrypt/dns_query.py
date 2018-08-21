# -*- coding: utf-8 -*-

import logging
from subprocess import check_output
from etc.settings import lista_soa

logging.basicConfig(filename='/tmp/validator.log', level=logging.DEBUG)

def retorna_root_domain(dominio):
    try:
        root_domain = check_output([
            'dig', '+nocmd', 'soa', dominio, '+noall', '+authority', '+answer']).rsplit()[0][:-1]
    except:
        return None
    else:
        return root_domain

def retorna_soa(dominio):
    try:
        resposta = check_output([
            'dig', '+nocmd', 'soa', dominio, '+noall', '+authority', '+answer']).split('\n')
    except:
        return None
    else:
        #soa = filter(lambda soa: True if "SOA" in soa else False, resposta)
        soa = [x.rsplit()[4][:-1] for x in resposta if "SOA" in x]
        return soa[0]

def retorna_ns(dominio):
    try:
        ns = check_output([
            'dig', '+nocmd', 'ns', retorna_root_domain(dominio), '+noall', '+answer']).rsplit()[4][:-1]
    except:
        return None
    else:
        return ns

def retorna_lista_ns(dominio):
    try:
        ns = check_output([
            'dig', '+nocmd', 'ns', retorna_root_domain(dominio), '+noall', '+answer']).split('\n')
    except:
        return None
    else:
        lista_ns = [x.rsplit()[4][:-1] for x in ns if "NS" in x]
        return lista_ns

def retorna_lista_txt(dominio):
    soa = retorna_soa(dominio)
    nserver = soa if soa in lista_soa else '8.8.8.8'
    try:
        txt = check_output([
            'dig', '+nocmd', 'txt', dominio, '@'+nserver, '+noall', '+answer']).split('\n')
    except:
        return None
    else:
        lista_txt = [x.rsplit()[4].replace('"', '') for x in txt if "TXT" in x]
        logging.info('hash(s) encontrados no dns: %s \n(dominio: %s | soa: %s | nserver: %s)' % (lista_txt, dominio, soa, nserver))
        return lista_txt
