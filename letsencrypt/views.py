# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

def index(request):
    return render(request, 'letsencrypt/index.html', {'help': True})

def certificado(request):
    if request.method != 'POST':
        return redirect('index')
    from letsencrypt_requester import Cert
    from oper_status_json import read_status_json, create_file

    cert_state = None
    dominio = request.POST['dominio']
    email = request.POST['email']
    alt_names = request.POST.getlist('alt_names')
    cert = Cert(dominio, email, alt_names=alt_names)

    try:
        status_json = read_status_json(cert.json_file)
    except Exception as erro:
        if hasattr(erro, 'strerror'):
            if erro.strerror == 'No such file or directory':
                from etc.settings import status_json_dir
                from time import time, strftime

                data = strftime("%d/%m/%Y %H:%M %Z")
                schema_json = {
                    'status': 'Solicitação enviada para fila',
                    'dominio': dominio,
                    'data da solicitação': data,
                    'email': email,
                    'alt_names': [x+dominio for x in alt_names]}
                create_file(cert.dominio, schema_json, status_json_dir)
                Cert.obtain_le_certificate.delay(cert)
                mensagem = 'Iniciando solicitação do certificado.'
                status = None
                cert_state = 'new_cert'
        else:
            mensagem = 'Houve um erro ao executar a solicitação.'
            status = {'erro': erro}
    else:
        if status_json['status'] == 'erro':
            status = status_json
            try:
                request.POST['confirm_delete']
            except:
                mensagem = """Encontrado um status de erro
                                referente a última solicitação.
                                Deletar status ?"""
                cert_state = 'erro_ask_delete'
            else:
                try:
                    from os import remove
                    remove(cert.json_file)
                except Exception as rm_erro:
                    mensagem = "Erro ao deletar."
                    status = None
                else:
                    mensagem = """Status deletado com sucesso. Inicie uma
                                nova solicitação de certificado."""
                    status = None
        elif status_json['status'] == 'validando hash':
            status = status_json
            mensagem = 'Solicitação em processo de validação.'
            cert_state = 'hash_validation'
        elif status_json['status'] == 'iniciando':
            status = status_json
            mensagem = 'Iniciando processo de validação.'
            cert_state = 'hash_validation'
        else:
            status = status_json
            mensagem = 'Status do processo.'
            cert_state = 'hash_validation'

    return render(request, 'letsencrypt/index.html', {
        'status': status,
        'email_post': email,
        'dominio_post': dominio,
        'mensagem': mensagem,
        'cert_state': cert_state})

def consulta(request):
    if request.method != 'POST':
        return redirect('index')
    from oper_status_json import read_status_json
    from letsencrypt_requester import Cert
    dominio = request.POST['dominio']
    cert = Cert(dominio, None)

    try:
        status_json = read_status_json(cert.json_file)
    except Exception as erro:
        if hasattr(erro, 'strerror') and erro.strerror == 'No such file or directory':
            mensagem = 'Não existe certificado para o domínio especificado.'
            status = None
    else:
        status = status_json
        mensagem = None

    return render(request, 'letsencrypt/index.html', {
                                                        'mensagem': mensagem,
                                                        'status': status,
                                                        'dominio': dominio
                                                      })

def status(request):
    import json
    try:
        with open('/var/www/html/certs/status/status.json', 'r') as file:
            status=json.load(file)
    except:
        status = None
    return render(request, 'letsencrypt/status.html', {'status': status})
