import webapp2
import httplib2

from urlparse import urlparse
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.appengine import StorageByKeyName
from model import Credentials


SCOPES = ('https://www.googleapis.com/auth/glass.timeline '
          'https://www.googleapis.com/auth/userinfo.profile')


class OAuthBaseRequestHandler(webapp2.RequestHandler):
""" base handler for Oauth requests """
  def create_oauth_flow(self):
    flow = flow_from_clientsecrets('client_secrets.json', scope=SCOPES)
    parsed_url = urlparse(self.request.url)
    flow.redirect_uri = '%s://%s/oauth2callback' % (parsed_url.scheme, parsed_url.netloc)
    return flow


class OAuthCodeRequestHandler(OAuthBaseRequestHandler):
""" handler for step1 of getting oauth creds """
  def get(self):
    flow = self.create_oauth_flow()
    'This line is to make switching between local and prodction environments transparent'
    url = flow.step1_get_authorize_url(redirect_uri=flow.redirect_uri)
    self.redirect(str(url))


class OAuthExchangeRequestHandler(OAuthBaseRequestHandler):

  def get(self):
    code = self.request.get('code')
    if not code:
      self.response.write('ERROR: Error getting auth code')
      return None
    oauth_flow = self.create_oauth_flow()

    try:
      creds = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
      self.response.write('ERROR: %s' % (FlowExchangeError))
      return None
    http = httplib2.Http()
    http = creds.authorize(http)
    users_service = build('oauth2', 'v2', http=http)
    user = users_service.userinfo().get().execute()
    
    userid = self.response.write(user.get('id'))
    StorageByKeyName(Credentials, userid, 'credentials').put(creds)


OAUTH_ROUTES = [
    ('/auth', OAuthCodeRequestHandler),
    ('/oauth2callback', OAuthExchangeRequestHandler),
    ]
