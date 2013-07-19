import sys
sys.path.insert(0, 'lib/')

import webapp2

from oauth_handler import OAUTH_ROUTES
from main_handler import MAIN_ROUTES

app = webapp2.WSGIApplication(MAIN_ROUTES+OAUTH_ROUTES)
