from base import BaseHandler

class RegisteHandler(BaseHandler):
	def get(self):
		open_registe = self.db.query("SELECT mvalue FROM maps WHERE mkey = 'registe'")
		if open_registe == "off":
			self.redirect("/")
		self.render("registe.html")
	def post(self):
		name = self.get_argument("name")
		password = self.get_argument("password")
		email = self.get_argument("email")
		self.db.execute("INSERT INTO authors (name,password,email) VALUES (%s,%s,%s)"
				,name,password,email)
		self.redirect("/auth/login")


