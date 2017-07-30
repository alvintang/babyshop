# """
# WSGI config for python project.
# https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
# """
#import sys
#import os

#from django.core.wsgi import get_wsgi_application

#sys.path.insert(0, '/django-app')

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

#application = get_wsgi_application()
import os, sys, site

site.addsitedir('/home/alvintang/webapps/babysetgo/babyshop/venv/lib/python3.5/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'base.settings'

activate_this = os.path.expanduser("/home/alvintang/webapps/babysetgo/babyshop/venv/bin/activate_this.py")
#execfile(activate_this, dict(__file__=activate_this))
exec(compile(open(activate_this, "rb").read(), activate_this, 'exec'), dict(__file__=activate_this))

# Calculate the path based on the location of the WSGI script
project = '/home/alvintang/webapps/babysetgo/'
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path = ['/home/alvintang/webapps/babysetgo/babyshop', '/home/alvintang/webapps/babysetgo/any_otherPaths?', '/home/alvintang/babysetgo/babyshop'] + sys.path

#from django.core.handlers.wsgi import WSGIHandler
#application = WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
