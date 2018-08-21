#! /usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import check_output
from etc.settings import status_json_dir
import os, json, sys
from celerytasks import app

@app.task
def gera_status():
    try:
        get_all = check_output(['certbot', 'certificates'])
    except Exception as erro:
        sys.exit()

    get_all = get_all.replace('- -', '')
    get_all = get_all.replace('/etc/letsencrypt', '')
    get_all = get_all.replace('Found the following certs:', '')
    get_all = get_all.lstrip()
    get_all = get_all.replace('  ', '')
    get_all = get_all.replace('VALID:', 'VALID')
    get_all = get_all.replace('Certificate Name: ', 'ENTRY Certificate Name: ')
    get_all = get_all.split('ENTRY ')

    if 'No certs found.\n \n' in get_all:
        return 'Não foram encontrados certificados'

    lista = []
    for x in get_all:
        if x:
            cert_name = x.split('\n')[0].split(': ')[1]
            domains = x.split('\n')[1].split(': ')[1]
            expiry = x.split('\n')[2].split(': ')[1]
            days = expiry.split(' (VALID ')[1].replace(' days)', '')
            cert_path = x.split('\n')[3].split(': ')[1]
            key_path = x.split('\n')[4].split(': ')[1]
            lista.append({
                'name': cert_name,
                'domains': domains,
                'expiry':expiry,
                'cert_path': cert_path,
                'key_path': key_path,
                'days': int(days)})

    lista_ordenada = sorted(lista, key=lambda days: days['days'])
    with open(os.path.join(status_json_dir, 'status/status.json'), 'w') as file:
        json.dump(lista_ordenada, file, indent=4)
    return 'Arquivo salvo: %s dominios' % len(lista_ordenada)

if __name__ == '__main__':
    gera_status()
