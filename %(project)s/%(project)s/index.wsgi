import os, sys
from os.path import dirname, basename, join, pardir

# activate the virtual environment
activate_this = '/srv/%(project)s/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# add self to pythonpath
django_settings_module = '%(project)s.settings'
pythonpath = [
    join(dirname(__file__), pardir),
]

# setup the project
sys.path = pythonpath + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = django_settings_module

# run the application
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# vim: set ft=python:

