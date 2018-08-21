#! /usr/bin/python
# -*- coding: utf-8 -*-

import atexit, zope, os, json, sys
from certbot import configuration, cli, plugins, reporter, util
from certbot.main import set_displayer
from oper_status_json import *
from celerytasks import app
from get_status import gera_status

class Cert():
    def __init__(self, dominio, email, **kwargs):
        self.dominio = limpa_dominio(dominio)
        self.certbot_live_dir = os.path.join('/etc/letsencrypt/live/', self.dominio)
        self.json_file = os.path.join('/var/www/html/certs', self.dominio, 'status.json')
        self.options = [
            'certonly',
            '--manual', '-n', '--agree-tos',
            '--email', email,
            '-d', self.dominio,
            #'--staging',
            '--expand',
            '--manual-public-ip-logging-ok',
            '--preferred-challenges', 'dns',
            '--manual-auth-hook',
            '/var/www/html/letsencrypt/validator.py '+self.dominio,
            '--manual-cleanup-hook', '/var/www/html/letsencrypt/cleanup.py']
        if 'staging' in kwargs:
            if kwargs['staging'] != None:
                self.options.append('--staging')
        if 'alt_names' in kwargs and kwargs['alt_names']:
                for alt_name in kwargs['alt_names']:
                    self.options.append('-d')
                    self.options.append(alt_name+self.dominio)

    def retorna_certificado(self):
        dominio = self.dominio
        certbot_live_dir = self.certbot_live_dir
        fullchain_file = os.path.join(certbot_live_dir, 'fullchain.pem')
        privkey_file = os.path.join(certbot_live_dir, 'privkey.pem')
        if os.path.isfile(fullchain_file) and os.path.isfile(privkey_file):
            with open(fullchain_file, 'r') as read_fullchain:
                fullchain = read_fullchain.read()
            with open(privkey_file, 'r') as read_privkey:
                privkey = read_privkey.read()
            return {'fullchain': fullchain, 'privkey': privkey}

    def write_certificate_to_json(self):
        pem = self.retorna_certificado()
        if pem is not None:
            fullchain_and_key = {
                                'fullchain':pem['fullchain'],
                                'privkey':pem['privkey'],
                                'status': 'certificado e chave privada gerados'}
            write_status_json(fullchain_and_key, self.json_file)
            del_status_json('erro', self.json_file)

    @app.task
    def obtain_le_certificate(self):
        options = self.options
        plugin = plugins.disco.PluginsRegistry.find_all()
        args = cli.prepare_and_parse_args(plugin, options)
        config = configuration.NamespaceConfig(args)
        zope.component.provideUtility(config)
        set_displayer(config)
        report = reporter.Reporter(config)
        zope.component.provideUtility(report)
        util.atexit.register(report.print_messages)
        try:
            config.func(config, plugin)
        except Exception as erro:
            msg = {'status': 'erro', 'erro': str(erro)}
            sys.path.append('/var/www/html/letsencrypt')
            from etc.settings import status_json_dir
            create_file(self.dominio, msg, status_json_dir)
        else:
            self.write_certificate_to_json()
            gera_status.delay()
