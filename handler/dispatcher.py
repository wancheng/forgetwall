from handler.base import BaseHandler

class DispatcherHandler(BaseHandler):
	def get(self):
		self.render(self.request.uri[1:])
