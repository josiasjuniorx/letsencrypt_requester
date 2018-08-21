#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, json

def write_status_json(dict_data, json_file):
    with open(json_file, 'r') as file:
        status_json = json.load(file)
    for key in dict_data:
        status_json[key] = dict_data[key]
    with open(json_file, 'w') as file:
        json.dump(status_json, file, indent=4, separators=(',', ':'))

def read_status_json(json_file):
    with open(json_file, 'r') as file:
        status_json = json.load(file)
    return status_json

def del_status_json(data_key, json_file):
    status_json = read_status_json(json_file)
    if status_json.has_key(data_key):
        del status_json[data_key]
        with open(json_file, 'w') as file:
            json.dump(status_json, file, indent=4, separators=(',', ':'))

def limpa_dominio(dominio):
    dominio_limpo = dominio.replace('*.', '')
    return dominio_limpo

def create_file(dominio, schema_json, status_json_dir):
    diretorio = os.path.join(status_json_dir, limpa_dominio(dominio))
    json_file = os.path.join(diretorio, 'status.json')
    if not os.path.isdir(diretorio):
        os.mkdir(os.path.join(diretorio))
    if not os.path.isfile(json_file):
        with open(json_file, 'w') as createfile:
            json.dump(schema_json, createfile, indent=4, separators=(',', ':'))
    else:
        write_status_json(schema_json, json_file)
    return json_file
