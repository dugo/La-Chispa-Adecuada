import os
import sys

path = '/var/webapps/lachispaadecuada'
if path not in sys.path:
    sys.path.append(path)

path = '/var/webapps'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'lachispaadecuada.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
