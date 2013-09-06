import tornado.web

from base import BaseHandler

class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)
	
class EntryHandler(BaseHandler):
	def get(self, slug):
		entry = self.db.get("SELECT a.*,b.name FROM entries AS a ,authors AS b WHERE a.author_id = b.id AND slug = %s", slug)
		if not entry: raise tornado.web.HTTPError(404)
		author = self.db.get("SELECT * FROM authors WHERE id = %s",int(entry.author_id))
		entry.username = author.name
		self.render("entry.html", entry=entry)



