from handler.base import BaseHandler

class Binding(BaseHandler):
	def get(self):
		self.render("weixin/binding.html")
