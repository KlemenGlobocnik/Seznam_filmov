#!/usr/bin/env python
import os
import jinja2
import webapp2
from Models import MoviesList


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("vstopna_stran.html")


class RezultatHandler(BaseHandler):
    def post(self):

        name = self.request.get("name")
        score = int(self.request.get("score"))
        url = self.request.get("url")
        image_url = self.request.get("image_url")

        movieslist = MoviesList(name=name, score=score, url=url, image_url=image_url)
        movieslist.put()

        params={"movieslist": movieslist}
        return self.render_template("rezultat.html", params=params)


class SeznamSporocilHandler(BaseHandler):
    def get(self):
        movieslist = MoviesList.query(MoviesList.deleted == False).fetch()
        params = {"movieslist": movieslist}
        return self.render_template("seznam_sporocil.html", params=params)

class SeznamSporocilVCakalniciHandler(BaseHandler):
    def get(self):
        movieslist = MoviesList.query(MoviesList.deleted == True).fetch()
        params = {"movieslist": movieslist}
        return self.render_template("seznam_sporocil_v_cakalnici.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        movie = MoviesList.get_by_id(int(sporocilo_id))
        params = {"movie": movie}
        return self.render_template("posamezno_sporocilo.html", params=params)

class PosameznoSporociloVCakalniciHandler(BaseHandler):
    def get(self, sporocilo_id):
        movie = MoviesList.get_by_id(int(sporocilo_id))
        params = {"movie": movie}
        return self.render_template("posamezno_sporocilo_v_cakalnici.html", params=params)


class UrediSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
            movie = MoviesList.get_by_id(int(sporocilo_id))
            params = {"movie": movie}
            return self.render_template("uredi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        new_name=self.request.get("name")
        new_score=int(self.request.get("score"))
        new_url=self.request.get("url")
        new_image_url=self.request.get("image_url")
        movie = MoviesList.get_by_id(int(sporocilo_id))
        movie.name=new_name
        movie.score=new_score
        movie.url=new_url
        movie.image_url=new_image_url
        movie.put()
        return self.redirect_to("seznam-sporocil")

class IzbrisiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        movie = MoviesList.get_by_id(int(sporocilo_id))
        params = {"movie": movie}
        return self.render_template("izbrisi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        movie = MoviesList.get_by_id(int(sporocilo_id))
        movie.deleted = True
        movie.put()
        return self.redirect_to("seznam-sporocil")

class PovrniSporociloHandler(BaseHandler):
    def post(self, sporocilo_id):
        movie = MoviesList.get_by_id(int(sporocilo_id))
        movie.deleted = False
        movie.put()
        return self.redirect_to("seznam-sporocil")

class DokoncnoIzbrisiSporociloHandler(BaseHandler):
    def post(self, sporocilo_id):
        movie = MoviesList.get_by_id(int(sporocilo_id))
        movie.key.delete()
        return self.redirect_to("seznam-sporocil")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam-sporocil', SeznamSporocilHandler, name="seznam-sporocil"),
    webapp2.Route('/sporocila-v-cakalnici', SeznamSporocilVCakalniciHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/sporocilo1/<sporocilo_id:\d+>', PosameznoSporociloVCakalniciHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/uredi', UrediSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/izbrisi', IzbrisiSporociloHandler),
    webapp2.Route('/sporocilo1/<sporocilo_id:\d+>/povrni', PovrniSporociloHandler),
    webapp2.Route('/sporocilo1/<sporocilo_id:\d+>/dokoncnoizbrisi', DokoncnoIzbrisiSporociloHandler),
], debug=True)