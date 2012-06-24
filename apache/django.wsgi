import os
import site
import sys

sys.path.append('/opt')
sys.path.append('/opt/owntube')
sys.path.append('/opt/owntube/owntube')
sys.path.append('/opt/owntube/owntube/vidoes')

site.addsitedir('/opt/owntube/lib/python2.6/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'owntube.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
