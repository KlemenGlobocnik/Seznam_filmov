from google.appengine.ext import ndb

class MoviesList(ndb.Model):
    name = ndb.StringProperty()
    score = ndb.IntegerProperty()
    url = ndb.StringProperty()
    image_url = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

