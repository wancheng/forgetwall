from handler.base import BaseHandler

class LoginHandler(BaseHandler):
	def get(self):
		if self.current_user:
			user_id = self.get_secure_cookie("www_forgetwall_come_user")
			if not user_id:
				self.render("admin/login.html")
			else:
				user = self.db.get("SELECT * FROM authors WHERE id = %s and isadmin = 1", int(user_id))
				if not user:
					self.render("admin/login.html")
				else:
					self.render("admin/index.html")
		else:
			self.render("admin/login.html")
	def post(self):
		username = self.get_argument("username")
		password = self.get_argument("password")
		admin = self.db.get("SELECT * FROM AUTHORS WHERE NAME= %s AND PASSWORD = %s AND ISADMIN = 1",username,password)
		if not admin:
			self.redirect("login")
		else:
			author_id = admin["id"]
			self.set_secure_cookie("www_forgetwall_com_user",str(author_id))
			self.redirect("index")
class IndexHandler(BaseHandler):
	def get(self):
		self.render("admin/index.html")
	def post(self):
		self.write("post")
