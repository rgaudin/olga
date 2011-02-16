#!/usr/bin/env python
# encoding=utf-8

import os
import sys
import django.core.handlers.wsgi

# add this file's folder + parent to path
file_dir = os.path.dirname(__file__)
file_parent_dir = os.sep.join(file_dir.rsplit(os.sep)[:-1])

sys.path.append(file_parent_dir)
sys.path.append(file_dir)

# Set the django settings and define the wsgi app
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' \
                                       % file_dir.split(os.sep)[-1]
application = django.core.handlers.wsgi.WSGIHandler()

# Mount the application to the url
applications = {'/': 'application'}

