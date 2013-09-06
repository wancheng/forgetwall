from base import BaseHandler

# class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
class AuthLoginHandler(BaseHandler):
	def get(self):
		if self.current_user:
			self.redirect(self.reverse_url('/'))
		else:
			self.render('login.html')
	
	def post(self):
		name = self.get_argument("name")
		password = self.get_argument("password")
		author = self.db.get("SELECT * FROM authors WHERE name = %s AND password = %s",
			name,password)
		if not author:
			self.redirect("/")
		else:
			author_id = author["id"]
			print author_id
			self.set_secure_cookie("www_forgetwall_com_user", str(author_id))
			self.redirect(self.get_argument("next", "/"))


