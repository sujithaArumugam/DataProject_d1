#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/flaskapp/code')

from flaskapp import app as application