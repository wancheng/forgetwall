from handler.base import BaseHandler

class IndexHandler(BaseHandler):
	def get(self):
		self.render("admin/wx_index.html")

	def post(self):
		self.write("post")
