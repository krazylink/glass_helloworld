import webapp2
import httplib2

from urlparse import urlparse
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

SCOPES = ('https://www.googleapis.com/auth/glass.timeline')


class OAuthBaseRequestHandler(webapp2.RequestHandler):

  def create_oauth_flow(self):
    flow = flow_from_clientsecrets('client_secrets.json', scope=SCOPES)
    parsed_url = urlparse(self.request.url)
    flow.redirect_uri = '%s://%s/oauth2callback' % (parsed_url.scheme, parsed_url.netloc)
    return flow


class OAuthCodeRequestHandler(OAuthBaseRequestHandler):

  def get(self):
    flow = self.create_oauth_flow()
    url = flow.step1_get_authorize_url(redirect_uri=flow.redirect_uri)
    self.redirect(str(url))


class OAuthExchangeRequestHandler(OAuthBaseRequestHandler):

  def get(self):
    code = self.request.get('code')
    print code
    if not code:
      self.response.write('ERROR: Error getting auth code')
      return None
    oauth_flow = self.create_oauth_flow()

    try:
      creds = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
      self.response.write('ERROR: %s' % (FlowExchangeError))
      return None
    self.redirect('/')


OAUTH_ROUTES = [
    ('/auth', OAuthCodeRequestHandler),
    ('/oauth2callback', OAuthExchangeRequestHandler),
    ]
