#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
from urllib import urlencode
from urlparse import parse_qs
from etc.settings import lista_soa
from dns_query import retorna_root_domain, retorna_soa

pdns = ['ns1.dominios.uol.com.br', 'ns2.dominios.uol.com.br', 'ns3.dominios.uol.com.br']
infoblox = []
url_pdns = '_REMOVIDO_' ## INSERIR URL DO PDNS

def is_ns_interno(dominio):
    soa = retorna_soa(dominio)
    if soa in pdns:
        return url_pdns
    elif soa in infoblox:
        return False
    else:
        return False

def criar_entrada(dominio, entrada, tipo, destino, acao='criar_entrada'):
    api_url = is_ns_interno(dominio)
    if api_url != False:
        req_url = {
            'acao': acao,
            'zona': retorna_root_domain(dominio),
            'entrada': entrada,
            'tipo': tipo,
            'destino': destino}
        req = requests.get(api_url+urlencode(req_url))
        return parse_qs(req.content)
    else:
        return {'mensagem': ['NS externo, necessario criar entrada manualmente'], 'retorno': ['9999']}

def excluir_entrada(dominio, entrada, tipo, destino, acao='excluir_entrada'):
    api_url = is_ns_interno(dominio)
    if api_url != False:
        req_url = {
            'acao': acao,
            'zona': retorna_root_domain(dominio),
            'entrada': entrada,
            'tipo': tipo,
            'destino': destino}
        req = requests.get(api_url+urlencode(req_url))
        return parse_qs(req.content)
    else:
        return {'mensagem': ['NS externo, necessario excluir entrada manualmente'], 'retorno': ['9999']}
