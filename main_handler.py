import webapp2


class MainPage(webapp2.RequestHandler):
  
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write('Hello, World!')
      self.response.write(dir(self))
      self.redirect('/auth')

MAIN_ROUTES = [
    ('/', MainPage),
    ]
