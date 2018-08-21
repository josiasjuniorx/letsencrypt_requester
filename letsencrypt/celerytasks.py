#! /usr/bin/python
# -*- coding: utf-8 -*-

from celery import Celery

app = Celery('letsencrypt')

app.config_from_object('celeryconfig')

if __name__ == '__main__':
    app.start()
