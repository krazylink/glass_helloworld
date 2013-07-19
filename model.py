from google.appengine.ext import db
from oauth2client.appengine import CredentialsProperty

class Credentials(db.Model):
  credentials = CredentialsProperty()
