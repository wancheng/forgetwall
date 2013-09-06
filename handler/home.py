from base import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT a.*,b.name FROM entries AS a, authors AS b WHERE a.author_id = b.id ORDER BY a.published "
                                "DESC LIMIT 5")
        self.render("home.html", entries=entries)
